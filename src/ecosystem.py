import asyncio
import logging
from typing import Dict, List, Any
from collections import defaultdict
import numpy as np
from datetime import datetime
import networkx as nx

from .agent import DeepScientificAgent
from .scientific_agent import KnowledgeBase, Hypothesis, HypothesisStatus
from .foundations import ScientificParadigm

class KnowledgeMarket:
    """
    Simulates a market for scientific knowledge where:
    1. Hypotheses have value
    2. Evidence serves as currency
    3. Paradigms act as market sectors
    4. Influence is capital
    """
    
    def __init__(self):
        self.hypothesis_prices: Dict[str, float] = {}
        self.evidence_currency: Dict[str, float] = {}
        self.paradigm_market_caps: Dict[ScientificParadigm, float] = defaultdict(float)
        self.trading_history: List[Dict[str, Any]] = []
        self.market_sentiment: float = 0.5  # 0-1, bearish to bullish
        
    async def value_hypothesis(self, hypothesis: Hypothesis) -> float:
        """Calculate market value of a hypothesis."""
        base_value = hypothesis.confidence * 100
        
        # Adjust for novelty (novel hypotheses are more valuable)
        novelty_bonus = hypothesis.novelty * 50
        
        # Adjust for testability (testable hypotheses are more actionable)
        testability_bonus = hypothesis.testability * 30
        
        # Adjust for empirical support
        evidence_value = len(hypothesis.supporting_evidence) * 20
        disevidence_cost = len(hypothesis.disconfirming_evidence) * 30
        
        total_value = base_value + novelty_bonus + testability_bonus + evidence_value - disevidence_cost
        
        # Apply market sentiment
        total_value *= (0.5 + self.market_sentiment)
        
        self.hypothesis_prices[hypothesis.id] = total_value
        return total_value
    
    async def trade_hypothesis(self, seller_agent_id: str, buyer_agent_id: str,
                             hypothesis: Hypothesis, price: float) -> bool:
        """Execute hypothesis trade between agents."""
        # Record trade
        trade = {
            "timestamp": datetime.now(),
            "seller": seller_agent_id,
            "buyer": buyer_agent_id,
            "hypothesis_id": hypothesis.id,
            "price": price,
            "hypothesis_confidence": hypothesis.confidence,
            "market_sentiment": self.market_sentiment
        }
        
        self.trading_history.append(trade)
        
        # Update market sentiment based on trade
        if price > 100:
            # High-value trade indicates bullish market
            self.market_sentiment = min(1.0, self.market_sentiment + 0.05)
        elif price < 30:
            # Low-value trade indicates bearish market
            self.market_sentiment = max(0.0, self.market_sentiment - 0.03)
        
        logging.info(f"Knowledge trade: {hypothesis.id} sold for {price:.1f} "
                    f"(sentiment: {self.market_sentiment:.3f})")
        
        return True

class ScientificEcosystem:
    """
    Ecosystem of deep scientific agents that:
    1. Compete and collaborate
    2. Exchange paradigms and methods
    3. Co-evolve research strategies
    4. Create emergent scientific progress
    """
    
    def __init__(self):
        self.agents: Dict[str, DeepScientificAgent] = {}
        self.communication_network = nx.DiGraph()  # Directed for influence flow
        self.knowledge_market = KnowledgeMarket()
        self.paradigm_ecology: Dict[ScientificParadigm, int] = defaultdict(int)
        self.evolutionary_pressure = 0.5
        self.innovation_rate = 0.3
        
        # Ecosystem metrics
        self.diversity_history: List[float] = []
        self.progress_history: List[float] = []
        self.convergence_history: List[float] = []
        
    def add_agent(self, agent: DeepScientificAgent, initial_influence: float = 1.0):
        """Add agent to ecosystem."""
        agent_id = f"{agent.domain}_{len(self.agents)}"
        self.agents[agent_id] = agent
        
        # Add to network with initial influence
        self.communication_network.add_node(agent_id, 
                                          influence=initial_influence,
                                          domain=agent.domain,
                                          paradigm=next(iter(agent.active_paradigms)).name)
        
        # Update paradigm ecology
        for paradigm in agent.active_paradigms:
            self.paradigm_ecology[paradigm] += 1
        
        logging.info(f"Added agent {agent_id} to ecosystem")
    
    async def run_ecosystem_evolution(self, generations: int = 5):
        """Run ecosystem evolution over multiple generations."""
        for gen in range(generations):
            logging.info(f"Ecosystem Generation {gen + 1}/{generations}")
            
            # 1. Agents conduct research
            await self._conduct_parallel_research()
            
            # 2. Knowledge exchange and trading
            await self._facilitate_knowledge_exchange()
            
            # 3. Paradigm competition and diffusion
            await self._simulate_paradigm_competition()
            
            # 4. Agent adaptation and learning
            await self._facilitate_agent_adaptation()
            
            # 5. Evolutionary pressure: success-based reproduction
            if gen % 2 == 0:  # Every other generation
                await self._apply_evolutionary_pressure()
            
            # 6. Record ecosystem state
            await self._record_ecosystem_state(gen)
    
    async def _conduct_parallel_research(self):
        """All agents conduct research in parallel."""
        tasks = []
        for agent_id, agent in self.agents.items():
            task = agent.enhanced_research_cycle(iterations=2)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful = 0
        for i, (agent_id, result) in enumerate(zip(self.agents.keys(), results)):
            if isinstance(result, Exception):
                logging.error(f"Agent {agent_id} research failed: {result}")
            else:
                successful += 1
        
        logging.info(f"{successful}/{len(self.agents)} agents completed research successfully")
        return results
    
    async def _facilitate_knowledge_exchange(self):
        """Facilitate knowledge exchange between agents."""
        # Agents with high influence share knowledge
        high_influence = self._get_high_influence_agents(3)
        
        for influencer_id in high_influence:
            influencer = self.agents.get(influencer_id)
            if not influencer:
                continue
            
            # Find agents to influence (those with lower influence)
            potential_influencees = [
                aid for aid in self.agents.keys()
                if (self.communication_network.nodes[aid].get("influence", 0) < 
                    self.communication_network.nodes[influencer_id].get("influence", 0))
            ]
            
            for influencee_id in potential_influencees[:2]:  # Influence top 2
                influencee = self.agents.get(influencee_id)
                if influencee:
                    await self._transfer_knowledge(influencer, influencee)
                    
                    # Update influence network
                    if not self.communication_network.has_edge(influencer_id, influencee_id):
                        self.communication_network.add_edge(influencer_id, influencee_id,
                                                          weight=0.5, type="knowledge_transfer")
                    else:
                        self.communication_network[influencer_id][influencee_id]["weight"] += 0.1
    
    async def _transfer_knowledge(self, source: DeepScientificAgent, 
                                 target: DeepScientificAgent):
        """Transfer knowledge from source to target agent."""
        # Transfer well-supported hypotheses
        well_supported = [h for h in source.active_hypotheses
                         if h.status in [HypothesisStatus.SUPPORTED, HypothesisStatus.WELL_SUPPORTED]]
        
        transferred = 0
        for hypothesis in well_supported[:2]:  # Transfer top 2
            # Create copy for target
            copied_hyp = Hypothesis(
                id=f"transferred_{hypothesis.id}_{datetime.now().timestamp()}",
                statement=hypothesis.statement,
                variables=hypothesis.variables,
                relationships=hypothesis.relationships,
                domain=hypothesis.domain,
                timestamp=datetime.now(),
                confidence=hypothesis.confidence * 0.8,  # Slightly reduced confidence
                complexity=hypothesis.complexity,
                novelty=hypothesis.novelty * 0.7,  # Less novel when transferred
                testability=hypothesis.testability
            )
            
            target.active_hypotheses.append(copied_hyp)
            transferred += 1
        
        if transferred > 0:
            logging.info(f"Transferred {transferred} hypotheses between agents")
    
    async def _simulate_paradigm_competition(self):
        """Simulate competition between scientific paradigms."""
        # Calculate paradigm fitness
        paradigm_fitness = await self._calculate_paradigm_fitness()
        
        # Paradigm with highest fitness gains adherents
        if paradigm_fitness:
            best_paradigm = max(paradigm_fitness.items(), key=lambda x: x[1])
            
            # Agents may switch to more successful paradigm
            for agent_id, agent in self.agents.items():
                current_paradigm = next(iter(agent.active_paradigms))
                current_fitness = paradigm_fitness.get(current_paradigm, 0)
                
                # Probability of switching based on fitness difference
                fitness_diff = best_paradigm[1] - current_fitness
                switch_prob = min(0.5, fitness_diff * self.evolutionary_pressure)
                
                if np.random.random() < switch_prob and best_paradigm[0] != current_paradigm:
                    # Agent switches paradigm
                    agent.active_paradigms = {best_paradigm[0]}
                    logging.info(f"Agent {agent_id} switched to {best_paradigm[0].name} paradigm")
                    
                    # Update paradigm ecology
                    self.paradigm_ecology[current_paradigm] = max(0, self.paradigm_ecology[current_paradigm] - 1)
                    self.paradigm_ecology[best_paradigm[0]] += 1
    
    async def _calculate_paradigm_fitness(self) -> Dict[ScientificParadigm, float]:
        """Calculate fitness of each paradigm in ecosystem."""
        paradigm_fitness = {}
        
        for paradigm in set(self.paradigm_ecology.keys()):
            # Get agents using this paradigm
            paradigm_agents = [
                agent for agent in self.agents.values()
                if paradigm in agent.active_paradigms
            ]
            
            if not paradigm_agents:
                continue
            
            # Calculate average success
            successes = []
            for agent in paradigm_agents:
                successful_hypotheses = len([
                    h for h in agent.active_hypotheses
                    if h.status in [HypothesisStatus.SUPPORTED, HypothesisStatus.WELL_SUPPORTED]
                ])
                total_hypotheses = len(agent.active_hypotheses)
                
                if total_hypotheses > 0:
                    successes.append(successful_hypotheses / total_hypotheses)
            
            if successes:
                avg_success = np.mean(successes)
                # Fitness based on success and number of adherents (network effects)
                adherents = len(paradigm_agents)
                paradigm_fitness[paradigm] = avg_success * (1 + np.log1p(adherents) * 0.1)
        
        return paradigm_fitness
    
    async def _facilitate_agent_adaptation(self):
        """Facilitate agent adaptation based on ecosystem performance."""
        # Calculate ecosystem-level metrics
        ecosystem_performance = await self._calculate_ecosystem_performance()
        
        # Adjust agent parameters based on ecosystem state
        for agent_id, agent in self.agents.items():
            # If ecosystem diversity is low, increase novelty preference
            if ecosystem_performance.get("diversity", 1) < 0.3:
                agent.novelty_preference = min(0.9, agent.novelty_preference + 0.1)
            
            # If convergence is high, increase risk tolerance for breakthroughs
            if ecosystem_performance.get("convergence", 0) > 0.7:
                agent.risk_tolerance = min(0.8, agent.risk_tolerance + 0.1)
    
    async def _calculate_ecosystem_performance(self) -> Dict[str, float]:
        """Calculate ecosystem-level performance metrics."""
        metrics = {
            "diversity": 0.0,
            "progress": 0.0,
            "convergence": 0.0,
            "innovation": 0.0
        }
        
        # Paradigm diversity
        total_agents = len(self.agents)
        if total_agents > 0:
            # Shannon diversity index for paradigms
            paradigm_counts = list(self.paradigm_ecology.values())
            total = sum(paradigm_counts)
            
            if total > 0:
                proportions = [c/total for c in paradigm_counts]
                shannon = -sum(p * np.log(p) for p in proportions if p > 0)
                max_shannon = np.log(len(paradigm_counts)) if paradigm_counts else 0
                
                metrics["diversity"] = shannon / max_shannon if max_shannon > 0 else 0
        
        # Progress (average hypothesis confidence)
        all_confidences = []
        for agent in self.agents.values():
            if agent.active_hypotheses:
                all_confidences.extend([h.confidence for h in agent.active_hypotheses])
        
        if all_confidences:
            metrics["progress"] = np.mean(all_confidences)
        
        # Convergence (agreement on hypotheses)
        if len(self.agents) > 1:
            # Check hypothesis overlap between agents
            all_hypotheses = []
            for agent in self.agents.values():
                agent_hypotheses = {h.statement for h in agent.active_hypotheses[:5]}  # Top 5
                all_hypotheses.append(agent_hypotheses)
            
            # Calculate Jaccard similarity between agents
            similarities = []
            for i in range(len(all_hypotheses)):
                for j in range(i+1, len(all_hypotheses)):
                    intersection = len(all_hypotheses[i] & all_hypotheses[j])
                    union = len(all_hypotheses[i] | all_hypotheses[j])
                    if union > 0:
                        similarities.append(intersection / union)
            
            if similarities:
                metrics["convergence"] = np.mean(similarities)
        
        return metrics
    
    async def _apply_evolutionary_pressure(self):
        """Apply evolutionary pressure: successful agents reproduce."""
        # Calculate agent fitness
        agent_fitness = []
        for agent_id, agent in self.agents.items():
            # Fitness based on hypothesis success and influence
            successful = len([h for h in agent.active_hypotheses
                            if h.status in [HypothesisStatus.SUPPORTED, HypothesisStatus.WELL_SUPPORTED]])
            total = len(agent.active_hypotheses)
            success_rate = successful / total if total > 0 else 0
            
            influence = self.communication_network.nodes[agent_id].get("influence", 1)
            
            fitness = success_rate * 0.7 + (influence / 10) * 0.3
            agent_fitness.append((agent_id, fitness))
        
        # Sort by fitness
        agent_fitness.sort(key=lambda x: x[1], reverse=True)
        
        # Top agents reproduce, bottom agents may die
        reproduction_cutoff = int(len(agent_fitness) * 0.3)  # Top 30% reproduce
        death_cutoff = int(len(agent_fitness) * 0.7)  # Bottom 30% at risk
        
        # Reproduction
        for i in range(min(2, reproduction_cutoff)):  # Top 2 reproduce
            parent_id, parent_fitness = agent_fitness[i]
            parent = self.agents[parent_id]
            
            # Create offspring with mutation
            offspring = await self._create_offspring(parent)
            
            # Ensure unique ID
            offspring_id = f"offspring_{parent_id}_{datetime.now().timestamp()}_{len(self.agents)}"
            
            self.agents[offspring_id] = offspring
            
            # Add to network with inherited influence
            self.communication_network.add_node(offspring_id,
                                              influence=parent_fitness * 0.8,
                                              domain=offspring.domain,
                                              paradigm=next(iter(offspring.active_paradigms)).name)
            
            # Connect to parent
            self.communication_network.add_edge(parent_id, offspring_id,
                                              weight=1.0, type="parent_offspring")
            
            logging.info(f"Agent {parent_id} reproduced -> {offspring_id}")
        
        # Death/removal
        if len(self.agents) > 10:  # Limit ecosystem size
            for i in range(len(agent_fitness)-1, max(len(agent_fitness)-3, death_cutoff), -1):
                if i < len(agent_fitness): # Bounds check
                    agent_id, fitness = agent_fitness[i]
                    if fitness < 0.2:  # Very low fitness
                        # Remove agent
                        if agent_id in self.agents:
                            del self.agents[agent_id]
                        if self.communication_network.has_node(agent_id):
                            self.communication_network.remove_node(agent_id)
                        logging.info(f"Agent {agent_id} removed (fitness: {fitness:.3f})")
    
    async def _create_offspring(self, parent: DeepScientificAgent) -> DeepScientificAgent:
        """Create offspring agent with inheritance and mutation."""
        # Inherit domain
        offspring_domain = parent.domain
        
        # Create knowledge base for offspring
        offspring_kb = KnowledgeBase()
        
        # Inherit some hypotheses from parent
        inherited_hypotheses = []
        for hypothesis in parent.active_hypotheses[:5]:  # Inherit top 5
            if hypothesis.confidence > 0.6:
                inherited_hypotheses.append(hypothesis)
        
        for hyp in inherited_hypotheses:
            offspring_kb.add_hypothesis(hyp)
        
        # Inherit paradigm with possible mutation
        parent_paradigm = next(iter(parent.active_paradigms))
        
        # Mutation: small chance of paradigm shift
        if np.random.random() < self.innovation_rate:
            # Choose different paradigm
            all_paradigms = list(ScientificParadigm)
            other_paradigms = [p for p in all_paradigms if p != parent_paradigm]
            if other_paradigms:
                offspring_paradigm = np.random.choice(other_paradigms)
            else:
                offspring_paradigm = parent_paradigm
        else:
            offspring_paradigm = parent_paradigm
        
        # Create offspring agent
        offspring = DeepScientificAgent(
            domain=offspring_domain,
            knowledge_base=offspring_kb,
            primary_paradigm=offspring_paradigm
        )
        
        # Inherit some parameters with mutation
        offspring.novelty_preference = parent.novelty_preference * np.random.uniform(0.9, 1.1)
        offspring.risk_tolerance = parent.risk_tolerance * np.random.uniform(0.9, 1.1)
        offspring.rigor_threshold = parent.rigor_threshold * np.random.uniform(0.95, 1.05)
        
        # Clamp values
        offspring.novelty_preference = max(0.1, min(0.9, offspring.novelty_preference))
        offspring.risk_tolerance = max(0.1, min(0.9, offspring.risk_tolerance))
        offspring.rigor_threshold = max(0.5, min(0.95, offspring.rigor_threshold))
        
        return offspring
    
    async def _record_ecosystem_state(self, generation: int):
        """Record current ecosystem state."""
        # Calculate metrics
        metrics = await self._calculate_ecosystem_performance()
        
        self.diversity_history.append(metrics["diversity"])
        self.progress_history.append(metrics["progress"])
        self.convergence_history.append(metrics["convergence"])
        
        # Log ecosystem state
        logging.info(f"Ecosystem Generation {generation}: "
                    f"Diversity: {metrics['diversity']:.3f}, "
                    f"Progress: {metrics['progress']:.3f}, "
                    f"Convergence: {metrics['convergence']:.3f}")
        
        # Paradigm distribution
        paradigm_dist = {p.name: c for p, c in self.paradigm_ecology.items() if c > 0}
        logging.info(f"Paradigm distribution: {paradigm_dist}")
    
    def _get_high_influence_agents(self, n: int = 3) -> List[str]:
        """Get agents with highest influence."""
        if not self.communication_network:
            return list(self.agents.keys())[:n]
        
        # Get influence scores
        influences = []
        for agent_id in self.agents.keys():
            if agent_id in self.communication_network:
                influence = self.communication_network.nodes[agent_id].get("influence", 0)
                # Add network centrality
                try:
                    # Use in-degree as proxy for influence if weighted
                    # or simple degree centrality
                    centrality = nx.degree_centrality(self.communication_network).get(agent_id, 0)
                except:
                    centrality = 0
                
                total_influence = influence * 0.7 + centrality * 0.3
                influences.append((agent_id, total_influence))
        
        # Sort by influence
        influences.sort(key=lambda x: x[1], reverse=True)
        
        return [agent_id for agent_id, _ in influences[:n]]

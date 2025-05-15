## pyTowerr - A Python Tower Defence 2D Game
#### Applications: Genetic Algorithms &amp; Reinforcement Learning
*Autor: António Raimundo*

Código-base para a Unidade Curricular (UC)
de Inteligência Artificial do Iscte-Sintra.

### Download do projeto
Para poderem fazer o _download_ do projeto, deverão seguir as instruções presentes na documentação do código-base. 
Após garantirem que o código-base já se encontra nas vossas máquinas, procedam para o
próximo passo.

### Configuração inicial
Têm de garantir que possuem os seguintes requisitos para poderem importar corretamente
o projeto-base para o vosso IDE (Visual Studio Code / PyCharm):
1. Ter a versão Python 3.11 ou superior instalada nas vossas máquinas.
2. Criar um ambiente virtual específico para este projeto. Para tal,
executem algumas operações:
   1. Atualizem a versão do Python Package Manager (pip): ``pip install --upgrade pip``;
   2. Criação do ambiente virtual (**recomendado**): ``conda create -n NOME_ESCOLHIDO python=3.11``;
   3. Configurar interpretador no VS Code ou PyCharm (se fizeram todos os passos corretamente, deverá aparecer nos vossos IDEs o novo ambiente virtual que criaram).

Após terminarem a configuração inicial, prossigam para mais uns comandos adicionais:

### Comandos iniciais:
Para garantir que o projeto base inicia sem problemas, devem importar o projeto, e no terminal 
(garantir que estão localizados na **pasta principal - pyTowerr**)
executem o seguinte comando:

``pip install -r requirements.txt``

### Ficheiro original `genetic_algorithm.py`:
Se houver necessidade de terem acesso ao código original do ficheiro `algorithms/genetic_algorithm.py`, têm abaixo a configuração base:
```python
import settings

class GeneticAlgorithm:
    def __init__(self, tower_type):
        self.num_generations = 5
        self.num_genes = 5  # accuracy, cooldown, range, damage, critical_chance
        self.population_size = 10
        self.tower_type = tower_type
        self.population = self.initialize_population()
        self.current_generation = 0

    def initialize_population(self):
        """
        Initialize the population with random values
        :return: list of lists, each containing the genes for an individual
        """
        # Get ranges for this tower type from settings
        range_min, range_max = settings.TOWER_TYPES[self.tower_type]['range']
        cooldown_min, cooldown_max = settings.TOWER_TYPES[self.tower_type]['cooldown']
        damage_min, damage_max = settings.TOWER_TYPES[self.tower_type]['damage']
        first_population = []

        # For demonstration purposes, we will initialize the population with the worst possible values
        for i in range(self.population_size):
            first_population.append([0.01, cooldown_max, range_min, damage_min, 0.0])  # Worst values
        return first_population

    def fitness_function(self, individual):
        """
        Calculate the fitness score for an individual
        :param individual: list of genes for an individual
        :return: float, the fitness score, between 0 and 1
        """
        return 0

    def run_generation(self):
        """
        Run a single generation of the genetic algorithm
        This is where the selection, crossover, and mutation steps are performed
        """
        pass

    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to produce a child
        :param parent1: Invividual 1 to crossover
        :param parent2: Individual 2 to crossover
        :return: list, the genes of the child (individual)
        """
        pass

    def mutate(self, individual):
        """
        Perform mutation on an individual
        :param individual: list, the genes of the individual to mutate
        :return: list, the genes of the mutated individual
        """
        pass

    def get_best_solution(self, num_solutions=1):
        """
        Get the best solution(s) from the final generation
        :param num_solutions: int, the number of best solutions to return (default is 1). Use 6 for the final solution
        :return: list of lists, the best solution(s) from the final generation. It should return 6 solutions for the 6 towers
        """
        pass

    def get_current_generation(self):
        """
        Get the current generation number
        :return: int, the current generation number
        """
        return self.current_generation

    def run(self):
        """
        Run the genetic algorithm for the specified number of generations.
        It uses the run_generation method to perform the steps for each generation
        """
        for i in range(self.num_generations):
            self.current_generation = i + 1
            self.run_generation()

```
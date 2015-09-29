import _PyPacwar
import numpy
import random
import operator


# Example Python module in C for Pacwar
def main():

	good_population = []
	for x in range(0,50):
		print "GA run#: " + str(x+1)
		good_population.append(run_GA([]))

	print ""

	best_gene = run_GA(good_population)
	print "Best Gene: " + best_gene
	# best_gene = "30022011131103123330231133202322103221230311223123"
	
	print ""

	# test "best" gene against 100 random ones. print stats
	num_wins = 0
	num_losses = 0
	num_rounds = 0
	num_remaining = 0
	for x in range(0,250):
		random_gene = generate_random_gene()

		(rounds,c1,c2) = _PyPacwar.battle(transform_string_to_array(best_gene), transform_string_to_array(random_gene))

		if c1 == 0:
			num_losses += 1
		else:
			num_wins += 1
			num_remaining += c1
			num_rounds += rounds
			
	percentage_win = 1.0*num_wins/250
	avg_rounds = 1.0*num_rounds/num_wins
	avg_remaining = 1.0*num_remaining/num_wins

	print "Num Wins: " + str(num_wins)
	print "Num Losses: " + str(num_losses)
	print "Percentage Win: " + str(percentage_win)
	print "Average Rounds to Win: " + str(avg_rounds)
	print "Average Remaining when Win:" + str(avg_remaining)



def run_GA(population):

	# generate random population of 50
	if len(population) == 0:
		for x in range(0,50):
			population.append(generate_random_gene())

	for run in range(0,100):
		# initialize score and freq dictionaries to 0 for each gene in random 
		# population
		population_to_score = {}
		population_to_freq = {}
		for gene in population:
			population_to_score[gene] = 0
			population_to_freq[gene] = 0

		# battle and score each random gene in population again random competitor
		random_competitor = generate_random_gene()

		for gene in population:
			(rounds, c1, c2) = _PyPacwar.battle(transform_string_to_array(gene), transform_string_to_array(random_competitor))
			population_to_score[gene] = score_battle(rounds, c1, c2)

		# find the sum of scores
		score_sum = 0
		for gene in population_to_score:
			score_sum += population_to_score[gene]

		# find the proportion of each score
		for gene in population_to_score:
			population_to_freq[gene] = population_to_score[gene]*1.0 / score_sum

		# sort population frequencies in desc order
		population_to_freq_sorted = sorted(population_to_freq.items(), key=operator.itemgetter(1), reverse=True)

		# selection for mating
		mating_pool = []
		for x in range(0,50):
			rand = random.random()
			cum_sum = 0
			for pair in population_to_freq_sorted:
				cum_sum += pair[1]
				if (cum_sum > rand):
					mating_pool.append(pair[0])
					break

		population = []
		while len(population) < 50:
			mom = mating_pool[random.randint(0, 49)]
			dad = mating_pool[random.randint(0, 49)]
			(child1, child2) = crossover(mom, dad)
			population.append(transform_array_to_string(child1))
			population.append(transform_array_to_string(child2))

	return population[random.randint(0,49)]

def generate_random_gene():
	gene = ""
	for x in range(0, 50):
		gene += str(random.randint(0,3))
	return gene

def score_battle(rounds, c1, c2):
	if (c2 == 0 and rounds < 100):
		return 20
	if (c2 == 0 and rounds >= 100 and rounds < 200):
		return 19
	if (c2 == 0 and rounds >= 200 and rounds < 300):
		return 18
	if (c2 == 0 and rounds >= 300 and rounds <= 500):
		return 17
	if (rounds > 500 and c1/c2 >= 10):
		return 13
	if (rounds > 500 and c1/c2 >= 3 and c1/c2 < 10):
		return 12
	if (rounds > 500 and c1/c2 >= 1.5 and c1/c2 < 3):
		return 11
	return 10

def transform_string_to_array(gene_string):
	gene_array = []
	for letter in gene_string:
		gene_array.append(int(letter))
	return gene_array

def transform_array_to_string(gene_array):
	gene_string = ""
	for g in gene_array:
		gene_string += str(g)
	return gene_string

def crossover(mom, dad):
	mom = transform_string_to_array(mom)
	dad = transform_string_to_array(dad)

	for i in range(0, len(mom)):
		rand = random.random()
		if (rand <= 0.05):
			temp_mom_i = mom[i]
			temp_dad_i = dad[i]
			mom[i] = temp_dad_i
			dad[i] = temp_mom_i

	return (mom, dad)


if __name__ == "__main__": main()

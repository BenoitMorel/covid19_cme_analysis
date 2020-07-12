#include "genesis/genesis.hpp"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <omp.h>
#include <stdexcept>
#include <cstdlib>
#include <algorithm>

using namespace genesis;
using namespace genesis::sequence;
using namespace genesis::tree;
using namespace genesis::utils;

void buildHistogram(Tree const &tree, std::string const &infile, std::string const &outfile) {
	std::vector<size_t> linkToEulerLeafIndex(tree.link_count());
	std::vector<size_t> eulerTourLeaves;
	for (auto it : eulertour(tree)) {
		if ( is_leaf(it.node()) ) {
			eulerTourLeaves.emplace_back(it.node().index());
		}
		linkToEulerLeafIndex[it.link().index()] = eulerTourLeaves.size();
	}

	double minLen = 0.0;
	/*
	// sort edges by their size
	std::vector<double> edgeLengths;
	for (size_t edgeId = 0; edgeId < tree.edge_count(); ++edgeId) {
		auto const& edge = tree.edge_at(edgeId);
		double len = edge.data<CommonEdgeData>().branch_length;
		edgeLengths.push_back(len);
	}
	std::sort(edgeLengths.begin(), edgeLengths.end(), std::greater<double>());
	minLen = edgeLengths[edgeLengths.size() / 10];
	*/

	size_t n = tree.node_count();

	if (!is_bifurcating(tree)) {
		throw std::runtime_error("The tree is not bifurcating");
	}

	std::vector<size_t> species;

#pragma omp parallel for schedule(dynamic)
	for (size_t edgeId = 0; edgeId < tree.edge_count(); ++edgeId) {
		auto const& edge = tree.edge_at(edgeId);

		if (edge.data<CommonEdgeData>().branch_length < minLen) {
			continue;
		}

		size_t linkIdx = edge.primary_link().index();

		size_t startLeafIndex = linkToEulerLeafIndex[linkIdx] % eulerTourLeaves.size();
		size_t endLeafIndex = linkToEulerLeafIndex[tree.link_at(linkIdx).outer().index()] % eulerTourLeaves.size();

		std::string outgroup;

		size_t i = startLeafIndex;
		while (i != endLeafIndex) {
			if (tree.node_at(eulerTourLeaves[i]).data<CommonNodeData>().name.empty()) {
				throw std::runtime_error("node name is empty");
			}
			outgroup += tree.node_at(eulerTourLeaves[i]).data<CommonNodeData>().name;
			i = (i + 1) % eulerTourLeaves.size();
			if (i != endLeafIndex) {
				outgroup += ",";
			}
		}

		std::string tempOutFilename = "tempOutFooBar_" + std::to_string(edge.index());

		std::cout << outgroup << std::endl;
		// found the outgroup, now we can call mptp
		std::string mptpCall = "software/mptp/bin/mptp --ml --tree_file " + infile + " --output_file " + tempOutFilename + " --multi --outgroup " + outgroup;
		int status = std::system(mptpCall.c_str());
		if (!WIFEXITED(status)) {
			throw std::runtime_error("Something went wrong while running mptp!");
		}
		// grab the number of species
		tempOutFilename = tempOutFilename + ".txt";

		std::ifstream infile(tempOutFilename);
		std::string line;
		std::getline(infile, line);
		std::getline(infile, line);
		std::getline(infile, line);
		std::getline(infile, line);
		std::getline(infile, line);
		line = line.substr(line.find(": ") + 2);
		species.emplace_back(atoi(line.c_str()));
		std::remove(tempOutFilename.c_str());
	}

	// create histogram
	std::vector<size_t> hist(n);

	std::ofstream output(outfile);
	for (size_t i = 0; i < species.size(); ++i) {
		hist[species[i]]++;
	}
	std::sort(species.begin(), species.end());
	size_t min_species = species[0];
	size_t max_species = species[species.size() - 1];
	size_t median_species = species[species.size() / 2]; // not truly median as in case of even number of trees we avoid taking the average between the two middle entries here.

	output << "Minimum species count: " << min_species << std::endl;
	output << "Maximum species count: " << max_species << std::endl;
	output << "Median species count: " << median_species << std::endl;

	output << std::endl << "Species count histogram (all computed using --ml option):" << std::endl;

	for (size_t i = 0; i < n; ++i) {
		if (hist[i] != 0) {
			output << i << "," << hist[i] << std::endl;
		}
	}
	output.close();
}

/**
 * The main method. Compare effects of different tree rooting on PTP species number.
 */
int main(int argc, char* argv[]) {
	std::ios_base::sync_with_stdio(false);
	std::cin.tie(NULL);

	// Get the files from command line
	if (argc != 3) {
		throw std::runtime_error(std::string( "Usage: " ) + argv[0] + " <tree-file> <output-file>");
	}
	std::string treePath = argv[1];
	std::string outputPath = argv[2];

	/*std::ifstream infile(outputPath);
	if (infile.good()) {
		std::cout << "ERROR: The specified output file already exists.\n";
		return 1;
	}*/

	//read tree
	auto tree = CommonTreeNewickReader().read( from_file( treePath ) );

	buildHistogram(tree, treePath, outputPath);
	return 0;
}

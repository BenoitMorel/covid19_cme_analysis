/*
    Copyright (C) 2020 Pierre Barbera

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact:
    Pierre Barbera <pierre.barbera@h-its.org>
    Exelixis Lab, Heidelberg Institute for Theoretical Studies
    Schloss-Wolfsbrunnenweg 35, D-69118 Heidelberg, Germany
*/

#include "genesis/genesis.hpp"

#include <iostream>
#include <string>
#include <unordered_map>
#include <numeric>
#include <vector>

using namespace genesis;
using namespace genesis::placement;
using namespace genesis::tree;
using namespace genesis::utils;

struct stats {
  double mean;
  double stddev;
};

std::ostream& operator<<( std::ostream& os, stats const& s )
{
  os << "  mean: " << std::to_string( s.mean ) << "\n";
  os << "  stdd: " << std::to_string( s.stddev ) << "\n";
  return os;
}

std::ostream& operator<<( std::ostream& os, std::unordered_map<std::string, size_t> const& map )
{
  for( auto const& elem : map ) {
    os << "  " << std::to_string(elem.second) << " x " << elem.first << "\n";
  }

  return os;
}

static stats get_stats(std::vector<double> const& v)
{

  auto stddevpair = mean_stddev(v);
  stats res;

  res.mean = stddevpair.mean;
  res.stddev = stddevpair.stddev;

  return res;
}

struct signal {
  size_t weak     = 0;
  size_t possible = 0;
  size_t strong   = 0;

  size_t sum() const { return weak + possible + strong; };

  std::vector<double> best_hits;
  std::vector<double> entropies;
  std::unordered_map<std::string, size_t> closest_hit_label;

};

constexpr double STRONG   = 0.5;
constexpr double WEAK     = 0.15;
constexpr double MAJORITY = 2.0 / 3.0;

static double get_entropy( Pquery const& pq )
{
  double entropy = 0.0;
  for( auto const& p : pq.placements() ) {
    auto lwr = p.like_weight_ratio;
    entropy += lwr * std::log2(lwr);
  }
  return -entropy;
}

/**
 *  Assumes input jplace files contain potential outgroups, evaluates their use for rooting.
 */
int main( int argc, char** argv )
{
  if( argc < 2 ) {
    throw std::runtime_error(
        std::string( "Usage: " ) + argv[ 0 ] + " <jplace-files...>\n" );
  }

  std::vector< std::string > jplace_files;
  for( int i = 1; i < argc; ++i ) {
    jplace_files.emplace_back( argv[ i ] );
  }
  SampleSet samples = JplaceReader().read( from_files( jplace_files ) );

  std::unordered_map< std::string, signal > results;
  // add entry for each outgroup in sample 0
  for( auto const& pq : samples[ 0 ] ) {
    auto const& name = pq.name_at( 0 );
    results[ name ];
  }

  auto const num_queries = samples[ 0 ].size();
  for( size_t i = 0; i < samples.size(); ++i ) {
    auto const& sample_name = samples.name_at( i );
    // std::cout << sample_name << "\n";
    auto& sample = samples[ i ];

    if( sample.size() != num_queries ) {
      throw std::runtime_error(
          std::string( "jplace files must have equal number of queries! Conflicting sample: " )
          + sample_name );
    }

    for( auto& pq : sample ) {
      auto const& name = pq.name_at( 0 ).name;
      auto elem        = results.find( name );

      // fail if samples don't contain the same queries
      if( elem == results.end() ) {
        throw std::runtime_error(
            std::string( "Samples don't contain the same queries.\nOffending Query: " ) 
            + name + "\nOffending Sample: " + sample_name );
      }
      auto& cur_signal = elem->second;

      sort_placements_by_weight( pq );

      auto const best_hit_lwr = pq.placement_at( 0 ).like_weight_ratio;

      if( best_hit_lwr > STRONG ) {
        cur_signal.strong++;
        auto const& edge = pq.placement_at( 0 ).edge();
        // get the label if there is one
        auto const& label = edge.secondary_node().data<PlacementNodeData>().name;
        cur_signal.closest_hit_label[label]++;
      } else if( best_hit_lwr < WEAK ) {
        cur_signal.weak++;
      } else {
        cur_signal.possible++;
      }

      cur_signal.best_hits.push_back( best_hit_lwr );
      
      normalize_weight_ratios( pq );
      cur_signal.entropies.push_back( get_entropy( pq ) );
    }
  }

  // print result
  for( auto const& result : results ) {
    auto const& query     = result.first;
    auto const& signal    = result.second;
    auto const sum        = signal.sum();
    size_t const majority = sum * MAJORITY;

    std::cout << query << ":\n";
    std::cout << "Best-Hit signal";
    if( signal.weak > majority ) {
      std::cout << " is majority \"weak\" (" << std::to_string( signal.weak ) << " / " << std::to_string( sum ) << ")\n";
    } else if( signal.possible > majority ) {
      std::cout << " is majority \"possible\" (" << std::to_string( signal.possible ) << " / " << std::to_string( sum ) << ")\n";
    } else if( signal.strong > majority ) {
      std::cout << " is majority \"strong\" (" << std::to_string( signal.strong ) << " / " << std::to_string( sum ) << "):\n";
      std::cout << signal.closest_hit_label;
    } else {
      std::cout << " is inconclusive ("
                << std::to_string( signal.strong ) << ", "
                << std::to_string( signal.possible ) << ", "
                << std::to_string( signal.weak ) << ")\n";
    }
    std::cout << "LWR Best Hit:\n";
    std::cout << get_stats(signal.best_hits);
    
    std::cout << "LWR Entropy:\n";
    std::cout << get_stats(signal.entropies);
    
    std::cout << "\n";
  }

  return 0;
}

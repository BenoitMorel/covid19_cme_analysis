/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2020 Lucas Czech

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
    Lucas Czech <lucas.czech@h-its.org>
    Exelixis Lab, Heidelberg Institute for Theoretical Studies
    Schloss-Wolfsbrunnenweg 35, D-69118 Heidelberg, Germany
*/

#include "genesis/genesis.hpp"

using namespace genesis;
using namespace genesis::tree;
using namespace genesis::utils;

#include <algorithm>
#include <limits>
#include <map>
#include <unordered_map>

static const Color base_gray_color = Color(0.8, 0.8, 0.8);

size_t get_position( std::vector<std::string> const& list, std::string const& entry )
{
    for( size_t i = 0; i < list.size(); ++i ) {
        if( utils::to_lower(list[i]) == utils::to_lower(entry) ) {
            return i;
            // return static_cast<double>(i) / static_cast<double>(list.size());
        }
    }
    throw std::runtime_error( "invalid entry " + entry );
    // LOG_ERR << "invalid entry " + entry ;
    return 0;
}

Color desaturate( Color const& color, double f )
{
    // Simple approximation of desaturation:
    // https://stackoverflow.com/questions/13328029/how-to-desaturate-a-color

    if( !( 0.0 <= f && f <= 1.0 ) ) {
        LOG_DBG << "desat " << f;
    }

    assert( 0.0 <= f && f <= 1.0 );
    return interpolate( color, base_gray_color, f );

    // auto const L = 0.3 * color.r() + 0.6 * color.g() + 0.1 * color.b();
    // auto const new_r = color.r() + f * (L - color.r());
    // auto const new_g = color.g() + f * (L - color.g());
    // auto const new_b = color.b() + f * (L - color.b());
    // return Color( new_r, new_g, new_b );
}

struct EdgeValues
{
    EdgeValues() = default;
    EdgeValues( double sum_, size_t count_, double min_, double max_ )
        : sum(sum_), count(count_), min(min_), max(max_)
    {}

    double sum   = 0.0;
    size_t count = 0;
    double min   = std::numeric_limits<double>::infinity();
    double max   = -std::numeric_limits<double>::infinity();
};

// Identical copy from genesis/tree/drawing/functions.cpp
// needed here as it is local in the original source file...
utils::SvgDocument get_color_tree_svg_doc_(
    CommonTree const&                tree,
    LayoutParameters const&          params,
    std::vector<utils::Color> const& color_per_branch
) {
    // Make a layout tree. We need a pointer to it in order to allow for the two different classes
    // (circular/rectancular) to be returned here. Make it a unique ptr for automatic cleanup.
    std::unique_ptr<LayoutBase> layout = [&]() -> std::unique_ptr<LayoutBase> {
        if( params.shape == LayoutShape::kCircular ) {
            return utils::make_unique<CircularLayout>( tree, params.type, params.ladderize );
        }
        if( params.shape == LayoutShape::kRectangular ) {
            return utils::make_unique<RectangularLayout>( tree, params.type, params.ladderize );
        }
        throw std::runtime_error( "Unknown Tree shape parameter." );
    }();

    // Set edge colors and strokes.
    if( ! color_per_branch.empty() ) {
        std::vector<utils::SvgStroke> strokes;
        for( auto const& color : color_per_branch ) {
            auto stroke = params.stroke;
            stroke.color = color;
            stroke.line_cap = utils::SvgStroke::LineCap::kRound;
            strokes.push_back( std::move( stroke ));
        }
        layout->set_edge_strokes( strokes );
    }

    // Prepare svg doc.
    auto svg_doc = layout->to_svg_document();
    svg_doc.margin.left = svg_doc.margin.top = svg_doc.margin.bottom = svg_doc.margin.right = 200;
    return svg_doc;
}

// Almost identical copy of the function from genesis/tree/drawing/functions.cpp
// but adapted to be able to set the height of the legend. 1.0 means full height (of the tree),
// and 0.5 means half the tree height, etc
void write_color_tree_to_svg_file(
    CommonTree const&                tree,
    LayoutParameters const&          params,
    std::vector<utils::Color> const& color_per_branch,
    std::vector<utils::Color> const& color_list,
    std::vector<std::string> const&  color_labels,
    double                           legend_height,
    std::string const&               svg_filename
) {
    // Get the basic svg tree layout.
    auto svg_doc = get_color_tree_svg_doc_( tree, params, color_per_branch );

    // Add the color legend / scale.

    // Make the color list.
    auto svg_color_list = make_svg_color_list( color_list, color_labels );

    // Move it to the bottom right corner.
    if( params.shape == LayoutShape::kCircular ) {
        svg_color_list.transform.append( utils::SvgTransform::Translate(
            1.2 * svg_doc.bounding_box().width() / 2.0, (0.5 - legend_height) * svg_doc.bounding_box().height()
        ));
        // svg_doc.margin.right = 0.2 * svg_doc.bounding_box().width() / 2.0 + 2 * svg_pal_settings.width + 200;
    }
    if( params.shape == LayoutShape::kRectangular ) {
        // This is just a prototype for this very specific analysis. We just want circular trees here.
        throw std::runtime_error("tree drawing only adapted for circular trees...");
    }

    // Apply a scale factor that scales the box to be half the figure height.
    // The denominator is the number items in the list times their height (15px, used by make_svg_color_list)
    auto const sf = ( legend_height * svg_doc.bounding_box().height() ) / (static_cast<double>( color_list.size() ) * 15.0 );
    svg_color_list.transform.append( utils::SvgTransform::Scale( sf ));

    // Add it to the svg doc.
    svg_doc.add( svg_color_list );

    // Write the whole svg doc to file.
    std::ofstream ofs;
    utils::file_output_stream( svg_filename, ofs );
    svg_doc.write( ofs );
}

void write_tree(
    Tree const& tree,
    std::vector<EdgeValues> edge_values,
    double min_value,
    double max_value,
    std::vector<Color> color_palette,
    std::vector<Color> color_list,
    std::vector<std::string> const& color_labels,
    double                          legend_height,
    std::string const& out_name
) {
    // Init with grey
    auto edge_colors = std::vector<Color>( tree.edge_count(), Color( 0.9, 0.9, 0.9 ));

    // double min_value = *std::min_element( edge_values.begin(), edge_values.end() );
    // double max_value = *std::max_element( edge_values.begin(), edge_values.end() );

    // Prepare a color mapping and a color normalization that brings all values between
    // min and max into the [0, 1] interval, so that we can nicely interpolate between them.
    auto map = ColorMap( color_palette );
    auto norm = ColorNormalizationLinear( min_value, max_value );
    LOG_DBG << "( min_value, max_value ); " << min_value << " " << max_value;

    // Now, we do a postorder traversal, filling in the inner edges with the average values
    // of their subtrees.
    for( auto const& it : postorder( tree )) {
        if( it.is_last_iteration() ) {
            continue;
        }
        if( is_leaf( it.edge() ) ) {
            // if( edge_values[it.edge().index()].count != 1 ) {
            //     LOG_DBG << "something is wrong with the edge indices for leaf nodes";
            // }
        } else {
            if( edge_values[it.edge().index()].count != 0 ) {
                LOG_DBG << "something is wrong with the edge indices for inner nodes";
            }
        }

        // We might have multifurcating trees, so we have to loop the full node here.
        // Loop over all edges of the subtrees of the current edge, and aggregate their values.
        for( auto const& nit : node_links( it.node() ) ) {
            // We skip the first iteration, which corresponds to the edge towards the root.
            // We are not doing this one yet.
            if( nit.is_first_iteration() ) {
                continue;
            }
            // if( edge_values[nit.edge().index()].count == 0 ) {
            //     LOG_DBG << "something is wrong with the edge indices for aggregates";
            // }

            if( edge_values[nit.edge().index()].count > 0 ) {
                if( std::isfinite(edge_values[nit.edge().index()].sum) ) {
                    edge_values[it.edge().index()].sum   += edge_values[nit.edge().index()].sum;
                    edge_values[it.edge().index()].count += edge_values[nit.edge().index()].count;
                }
                if( std::isfinite(edge_values[nit.edge().index()].min) ) {
                    edge_values[it.edge().index()].min    = std::min(
                        edge_values[it.edge().index()].min,
                        edge_values[nit.edge().index()].min
                    );
                }
                if( std::isfinite(edge_values[nit.edge().index()].max) ) {
                    edge_values[it.edge().index()].max    = std::max(
                        edge_values[it.edge().index()].max,
                        edge_values[nit.edge().index()].max
                    );
                }
            }
        }

        // Now we have all values for the current edge, and can hence calculate its color.
        double const value
            = edge_values[it.edge().index()].sum
            / static_cast<double>( edge_values[it.edge().index()].count )
        ;
        double const desat
            = ( edge_values[it.edge().index()].max - edge_values[it.edge().index()].min )
            / ( max_value - min_value )
        ;
        if( std::isfinite(value) && std::isfinite(desat) ) {
            // LOG_DBG1 << value;
            edge_colors[it.edge().index()] = desaturate( map( norm, value ), desat );
        } else{
            edge_colors[it.edge().index()] = base_gray_color;

            // LOG_DBG << "value    " << value;
            // LOG_DBG << "edge min " << edge_values[it.edge().index()].min;
            // LOG_DBG << "edge max " << edge_values[it.edge().index()].max;
            // LOG_DBG << "abs min  " << min_value;
            // LOG_DBG << "abs max  " << max_value;
        }
    }

    // Draw the tree. Params can be adjusted if needed, e.g., stroke width for the svg
    LayoutParameters params;
    params.stroke.width = 12.0;
    if( color_labels.empty() ) {
        write_color_tree_to_svg_file(
            tree, params, edge_colors, map, norm, out_name
        );
    } else {
        if( color_list.empty() ) {
            color_list = ColorMap( color_palette ).color_list( color_labels.size() );
        }
        write_color_tree_to_svg_file(
            tree, params, edge_colors, color_list, color_labels, legend_height, out_name
        );
    }
}

void run_with_metdata( std::string const& tree_file, std::string const& meta_file, std::string const& out_prefix )
{
    // Read tree
    auto const tree = CommonTreeNewickReader().read( from_file( tree_file ));
    LOG_INFO << "Found tree with " << leaf_node_count( tree ) << " tips in tree file";

    // Test. Print all leaf node names.
    // for( auto const& node : tree.nodes() ) {
    //     if( is_leaf(node) ) {
    //         LOG_BOLD << node.data<CommonNodeData>().name;
    //     }
    // }

    // Read metadata. We use the default reader settings, which assumes the first row contains
    // the column names of the metadata fields, and the first column contains the names that
    // correspond to the tree leaf names.
    auto data = DataframeReader<std::string>('\t').read( from_file( meta_file ));
    LOG_INFO << "Found " << data.cols() << " meta data columns with " << data.rows() << " entries.";

    // For each column, make a new tree visualization
    for( size_t i = 0; i < data.cols(); ++i ) {

        // Prepare a vector that collects all needed values for the edges, which we use to aggregate
        // and average for the inner edges of the tree, so that they represent their subtrees.
        // Each entry corresponds to an edge index, and contains the sum of all values in the subtree,
        // the number of edges in the subtree, and the min and max values in the subtree.
        // For example: An edge that leads to a leaf node contains just its metadata value and 1
        // edge count, while an edge that leads to a cherry contains the sum of both edges below
        // it and the count 2.
        // By doing this, we can easily aggregate and calculate averages later,
        // as well as compare these to the min and max to desaturate as needed.
        std::vector<EdgeValues> edge_values( tree.edge_count() );

        // Also, when the column cannot be converted to numbers, we cannot make a color gradient
        // as a legend next to the tree, but instead want a simple list of colors. So, for this case,
        // we here prepare a list of labels for this color list, and fill it if we find a string
        // column. In that case, a filled list is later used as an indicator that we indeed want to
        // make a list instead of a gradient.
        std::vector<std::string> color_labels;

        // In order to map values to colors, we need the min and max value that occur in the column.
        double min_value = std::numeric_limits<double>::infinity();
        double max_value = -std::numeric_limits<double>::infinity();

        // Treat the column as a list of strings, where we visualize each string with its own color.
        // For this, we make a list of them, sort it, and give colors in alphabetical order.
        // In the future, we can also give colors in some other order that looks better
        // or makes more sense (country names ordered by location, for example).
        LOG_INFO << summarize_column( data, i );

        auto const& data_col = data[i].as<std::string>();

        // Make a map of all strings in the column, sorted. Then, give them their corresponding
        // index. We could use a sorted vector for this, but lookup would be slower than
        // using a map.
        std::map<std::string, size_t, NaturalLess<>> value_map;
        std::map<std::string, size_t, NaturalLess<>> value_map_counts;
        for( auto const& v : data_col ) {
            value_map[v] = 0;
            ++value_map_counts[v];
        }
        size_t cnt = 0;
        for( auto& v : value_map ) {
            color_labels.push_back( v.first + "  (" + std::to_string( value_map_counts[v.first] ) + ")" );
            v.second = cnt;
            ++cnt;
        }
        min_value = 0;
        max_value = value_map.size() - 1;

        // Fill the edge values with the values the we just mapped to numbers
        for( size_t e = 0; e < tree.edge_count(); ++e ) {
            if( is_leaf( tree.edge_at(e)) ) {
                auto const& name = tree.edge_at(e).secondary_node().data<CommonNodeData>().name;
                if( !data.has_row_name( name ) ) {
                    throw std::runtime_error( "No metadata row for leaf node " + name );
                }
                auto const val = static_cast<double>(value_map[data_col[name]]);
                edge_values[e] = { val, 1, val, val };
            }
        }

        write_tree(
            tree, edge_values, min_value, max_value, color_list_nextstrain(),
            ColorMap( color_list_nextstrain() ).color_list(color_labels.size()), color_labels, 0.5,
            out_prefix + data[i].name() + ".svg"
        );
    }
}

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "Started";

    // Get the files from command line
    if( argc != 4 ) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <input-tree-newick> <input-metadata-csv> <output-tree-prefix>"
        );
    }
    auto const tree_file = std::string( argv[1] );
    auto const meta_file = std::string( argv[2] );
    auto const out_prefix = std::string( argv[3] );
    run_with_metdata( tree_file, meta_file, out_prefix );

    LOG_INFO << "Finished";
    return 0;
}

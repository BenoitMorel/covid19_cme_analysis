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

static std::vector<std::string> region_order = {
    "Asia",
    "Oceania",
    "Africa",
    "Europe",
    "South America",
    // "Central America",
    "North America"
};

static std::vector<std::string> country_order = {
    "Algeria",
    "Australia",
    "Belgium",
    "Brazil",
    "Cambodia",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Congo",
    "Czech Republic",
    "Denmark",
    "Ecuador",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Greece",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Ireland",
    "Italy",
    "Japan",
    "Kuwait",
    "Luxembourg",
    "Malaysia",
    "Mexico",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Pakistan",
    "Panama",
    "Poland",
    "Portugal",
    "Russia",
    "Saudi Arabia",
    "Senegal",
    "Singapore",
    "Slovakia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "USA",
    "United Kingdom",
    "Vietnam"

    // "Mongolia",
    // "China",
    // "Hong Kong",
    // "Taiwan",
    // "Philippines",
    // "Japan",
    // "South Korea",
    // "Nepal",
    // "India",
    // "Bangladesh",
    // "Sri Lanka",
    // "Vietnam",
    // "Cambodia",
    // "Thailand",
    // "Myanmar",
    // "Malaysia",
    // "Singapore",
    // "Brunei",
    // "Indonesia",
    // "Guam",
    // "Timor-Leste",
    // "Australia",
    // "New Zealand",
    // "Saudi Arabia",
    // "Qatar",
    // "United Arab Emirates",
    // "Kuwait",
    // "Lebanon",
    // "Oman",
    // "Iran",
    // "Israel",
    // "Jordan",
    // "Turkey",
    // "Pakistan",
    // "Kazakhstan",
    // "Kyrgyzstan",
    // "Georgia",
    // "Russia",
    // "Serbia",
    // "Romania",
    // "Europe",
    // "Latvia",
    // "Slovakia",
    // "Slovenia",
    // "Bosnia and Herzegovina",
    // "Poland",
    // "Belarus",
    // "Estonia",
    // "Lithuania",
    // "Bulgaria",
    // "Hungary",
    // "Croatia",
    // "France",
    // "Iceland",
    // "Norway",
    // "Denmark",
    // "Netherlands",
    // "Belgium",
    // "Luxembourg",
    // "Germany",
    // "Austria",
    // "Switzerland",
    // "Italy",
    // "Cyprus",
    // "Spain",
    // "Czech Republic",
    // "United Kingdom",
    // "Ireland",
    // "Finland",
    // "Sweden",
    // "Portugal",
    // "Greece",
    // "Egypt",
    // "Nigeria",
    // "Benin",
    // "Kenya",
    // "Ghana",
    // "Senegal",
    // "Gambia",
    // "Algeria",
    // "Tunisia",
    // "Morocco",
    // "Uganda",
    // "Democratic Republic of the Congo",
    // "Congo",
    // "South Africa",
    // "Chile",
    // "Ecuador",
    // "Peru",
    // "Brazil",
    // "Argentina",
    // "Venezuela",
    // "Uruguay",
    // "Colombia",
    // "Panama",
    // "Costa Rica",
    // "Mexico",
    // "Jamaica",
    // "USA",
    // "Canada"
};

static std::vector<std::string> country_order_dimitrios = {
    "Mongolia",
    "China",
    "WUHAN",
    "BEIJING",
    "CHONGQING",
    "FOSHAN",
    "FUJIAN",
    "FUYANG",
    "GUANGDONG",
    "GUANGZHOU",
    "HANGZHOU",
    "JIAN",
    "JIANGSU",
    "JINGZHOU",
    "NANCHANG",
    "PINGXIANG",
    "SHANDONG",
    "SHANGHAI",
    "SHANGRAO",
    "SHENZHEN",
    "SICHUAN",
    "TIANMEN",
    "XINYU",
    "YUNNAN",
    "HongKong",
    "Taiwan",
    "Philippines",
    "Japan",
    "SouthKorea",
    "KOREA",
    "Nepal",
    "India",
    "Bangladesh",
    "SriLanka",
    "Vietnam",
    "Cambodia",
    "Thailand",
    "Myanmar",
    "Malaysia",
    "Singapore",
    "Brunei",
    "Indonesia",
    "Guam",
    "Timor-Leste",
    "Australia",
    "NewZealand",
    "SaudiArabia",
    "Qatar",
    "UnitedArabEmirates",
    "Kuwait",
    "Lebanon",
    "Oman",
    "Iran",
    "Israel",
    "Jordan",
    "Turkey",
    "Pakistan",
    "Kazakhstan",
    "Kyrgyzstan",
    "Georgia",
    "Russia",
    "Serbia",
    "Romania",
    "Europe",
    "Latvia",
    "Slovakia",
    "Slovenia",
    "BosniaandHerzegovina",
    "Poland",
    "Belarus",
    "Estonia",
    "Lithuania",
    "Bulgaria",
    "Hungary",
    "Croatia",
    "France",
    "Iceland",
    "Norway",
    "Denmark",
    "Netherlands",
    "Belgium",
    "Luxembourg",
    "Germany",
    "Austria",
    "Switzerland",
    "Italy",
    "Cyprus",
    "Spain",
    "CzechRepublic",
    "UnitedKingdom",
    "ENGLAND",
    "SCOTLAND",
    "WALES",
    "Ireland",
    "Finland",
    "Sweden",
    "Portugal",
    "Greece",
    "Egypt",
    "Nigeria",
    "Benin",
    "Kenya",
    "Ghana",
    "Senegal",
    "Gambia",
    "Algeria",
    "Tunisia",
    "Morocco",
    "Uganda",
    "DemocraticRepublicoftheCongo",
    "DRC",
    "Congo",
    "SouthAfrica",
    "Chile",
    "Ecuador",
    "Peru",
    "Brazil",
    "Argentina",
    "Venezuela",
    "PUERTORICO",
    "Uruguay",
    "Colombia",
    "Panama",
    "CostaRica",
    "Mexico",
    "Jamaica",
    "USA",
    "Canada",
    "ENV",
    "MINK"
};

static std::unordered_map<std::string, std::string> country_to_region = {
    { "MONGOLIA", "Asia" },
    { "CHINA", "Asia" },
    { "WUHAN", "Asia" },
    { "BEIJING", "Asia" },
    { "CHONGQING", "Asia" },
    { "FOSHAN", "Asia" },
    { "FUJIAN", "Asia" },
    { "FUYANG", "Asia" },
    { "GUANGDONG", "Asia" },
    { "GUANGZHOU", "Asia" },
    { "HANGZHOU", "Asia" },
    { "JIAN", "Asia" },
    { "JIANGSU", "Asia" },
    { "JINGZHOU", "Asia" },
    { "NANCHANG", "Asia" },
    { "PINGXIANG", "Asia" },
    { "SHANDONG", "Asia" },
    { "SHANGHAI", "Asia" },
    { "SHANGRAO", "Asia" },
    { "SHENZHEN", "Asia" },
    { "SICHUAN", "Asia" },
    { "TIANMEN", "Asia" },
    { "XINYU", "Asia" },
    { "YUNNAN", "Asia" },
    { "HONGKONG", "Asia" },
    { "TAIWAN", "Asia" },
    { "PHILIPPINES", "Asia" },
    { "JAPAN", "Asia" },
    { "SOUTHKOREA", "Asia" },
    { "KOREA", "Asia" },
    { "NEPAL", "Asia" },
    { "INDIA", "Asia" },
    { "BANGLADESH", "Asia" },
    { "SRILANKA", "Asia" },
    { "VIETNAM", "Asia" },
    { "CAMBODIA", "Asia" },
    { "THAILAND", "Asia" },
    { "MYANMAR", "Asia" },
    { "MALAYSIA", "Asia" },
    { "SINGAPORE", "Asia" },
    { "BRUNEI", "Asia" },
    { "INDONESIA", "Asia" },

    { "SAUDIARABIA", "Asia" },
    { "QATAR", "Asia" },
    { "UNITEDARABEMIRATES", "Asia" },
    { "KUWAIT", "Asia" },
    { "LEBANON", "Asia" },
    { "OMAN", "Asia" },
    { "IRAN", "Asia" },
    { "ISRAEL", "Asia" },
    { "JORDAN", "Asia" },
    { "TURKEY", "Asia" },
    { "PAKISTAN", "Asia" },
    { "KAZAKHSTAN", "Asia" },
    { "KYRGYZSTAN", "Asia" },
    { "GEORGIA", "Asia" },
    { "RUSSIA", "Asia" },

    { "GUAM", "Oceania" },
    { "TIMOR-Leste", "Oceania" },
    { "AUSTRALIA", "Oceania" },
    { "NEWZEALAND", "Oceania" },

    { "SERBIA", "Europe" },
    { "ROMANIA", "Europe" },
    { "EUROPE", "Europe" },
    { "LATVIA", "Europe" },
    { "SLOVAKIA", "Europe" },
    { "SLOVENIA", "Europe" },
    { "BOSNIAANDHERZEGOVINA", "Europe" },
    { "POLAND", "Europe" },
    { "BELARUS", "Europe" },
    { "ESTONIA", "Europe" },
    { "LITHUANIA", "Europe" },
    { "BULGARIA", "Europe" },
    { "HUNGARY", "Europe" },
    { "CROATIA", "Europe" },
    { "FRANCE", "Europe" },
    { "ICELAND", "Europe" },
    { "NORWAY", "Europe" },
    { "DENMARK", "Europe" },
    { "NETHERLANDS", "Europe" },
    { "BELGIUM", "Europe" },
    { "LUXEMBOURG", "Europe" },
    { "GERMANY", "Europe" },
    { "AUSTRIA", "Europe" },
    { "SWITZERLAND", "Europe" },
    { "ITALY", "Europe" },
    { "CYPRUS", "Europe" },
    { "SPAIN", "Europe" },
    { "CZECHREPUBLIC", "Europe" },
    { "UNITEDKINGDOM", "Europe" },
    { "ENGLAND", "Europe" },
    { "SCOTLAND", "Europe" },
    { "WALES", "Europe" },
    { "IRELAND", "Europe" },
    { "FINLAND", "Europe" },
    { "SWEDEN", "Europe" },
    { "PORTUGAL", "Europe" },
    { "GREECE", "Europe" },

    { "EGYPT", "Africa" },
    { "NIGERIA", "Africa" },
    { "BENIN", "Africa" },
    { "KENYA", "Africa" },
    { "GHANA", "Africa" },
    { "SENEGAL", "Africa" },
    { "GAMBIA", "Africa" },
    { "ALGERIA", "Africa" },
    { "TUNISIA", "Africa" },
    { "MOROCCO", "Africa" },
    { "UGANDA", "Africa" },
    { "DEMOCRATICREPUBLICOFTHECONGO", "Africa" },
    { "DRC", "Africa" },
    { "CONGO", "Africa" },
    { "SOUTHAFRICA", "Africa" },

    { "CHILE", "South America" },
    { "ECUADOR", "South America" },
    { "PERU", "South America" },
    { "BRAZIL", "South America" },
    { "ARGENTINA", "South America" },
    { "VENEZUELA", "South America" },
    { "URUGUAY", "South America" },
    { "COLOMBIA", "South America" },

    { "PUERTORICO", "North America" },
    { "PANAMA", "North America" },
    { "COSTARICA", "North America" },
    { "JAMAICA", "North America" },
    { "MEXICO", "North America" },
    { "USA", "North America" },
    { "CANADA", "North America" }

    // { "ENV", "N/A" },
    // { "MINK", "N/A" }
};

size_t get_position( std::vector<std::string> const& list, std::string const& entry )
{
    for( size_t i = 0; i < list.size(); ++i ) {
        if( utils::to_lower(list[i]) == utils::to_lower(entry) ) {
            return i;
            // return static_cast<double>(i) / static_cast<double>(list.size());
        }
    }
    // throw std::runtime_error( "invalid entry " + entry );
    LOG_ERR << "invalid entry " + entry ;
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
    auto const L = 0.3 * color.r() + 0.6 * color.g() + 0.1 * color.b();
    auto const new_r = color.r() + f * (L - color.r());
    auto const new_g = color.g() + f * (L - color.g());
    auto const new_b = color.b() + f * (L - color.b());
    return Color( new_r, new_g, new_b );
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

void write_tree(
    Tree const& tree,
    std::vector<EdgeValues> edge_values,
    double min_value,
    double max_value,
    std::vector<std::string> const& color_labels,
    std::vector<Color> color_list,
    std::string const& out_name
) {
    // Init with grey
    auto edge_colors = std::vector<Color>( tree.edge_count(), Color( 0.9, 0.9, 0.9 ));

    // double min_value = *std::min_element( edge_values.begin(), edge_values.end() );
    // double max_value = *std::max_element( edge_values.begin(), edge_values.end() );

    // Prepare a color mapping and a color normalization that brings all values between
    // min and max into the [0, 1] interval, so that we can nicely interpolate between them.
    auto map = ColorMap( color_list );
    auto norm = ColorNormalizationLinear( min_value, max_value );
    LOG_DBG << "( min_value, max_value ); " << min_value << " " << max_value;

    // Now, we do a postorder traversal, filling in the inner edges with the average values
    // of their subtrees.
    for( auto const& it : postorder( tree )) {
        if( it.is_last_iteration() ) {
            continue;
        }
        if( is_leaf( it.edge() ) ) {
            if( edge_values[it.edge().index()].count != 1 ) {
                LOG_DBG << "something is wrong with the edge indices for leaf nodes";
            }
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
            edge_colors[it.edge().index()] = Color(0.8, 0.8, 0.8);

            LOG_DBG << "value    " << value;
            LOG_DBG << "edge min " << edge_values[it.edge().index()].min;
            LOG_DBG << "edge max " << edge_values[it.edge().index()].max;
            LOG_DBG << "abs min  " << min_value;
            LOG_DBG << "abs max  " << max_value;
        }
    }

    // Draw the tree. Params can be adjusted if needed, e.g., stroke width for the svg
    LayoutParameters params;
    params.stroke.width = 8.0;
    if( color_labels.empty() ) {
        write_color_tree_to_svg_file(
            tree, params, edge_colors, map, norm, out_name
        );
    } else {
        write_color_tree_to_svg_file(
            tree, params, edge_colors, map.color_list( color_labels.size() ), color_labels, out_name
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

        // Convert metadata to numercial where possible. In the future, we can also do other data types,
        // bool, int, tine/data, geo location, etc...
        // Then, fill the edge values with the data
        if( to_lower(data.col_name(i)) == "region" || to_lower(data.col_name(i)) == "country" ) {
            LOG_INFO << summarize_column( data, i );
            auto const& data_col = data[i].as<std::string>();

            if( to_lower(data.col_name(i)) == "region" ) {
                color_labels = region_order;
            } else if( to_lower(data.col_name(i)) == "country"  ) {
                color_labels = country_order;
            }
            // min_value = 0;
            // max_value = color_labels.size() - 1;

            // make a list of values found, just to test that our order lists contain the same elements.
            std::set<std::string> check_list;

            // Fill the edge values with the values the we just mapped to numbers
            for( size_t e = 0; e < tree.edge_count(); ++e ) {
                if( is_leaf( tree.edge_at(e)) ) {
                    auto const& name = tree.edge_at(e).secondary_node().data<CommonNodeData>().name;
                    if( !data.has_row_name( name ) ) {
                        throw std::runtime_error( "No metadata row for leaf node " + name );
                    }

                    // Get the index of the entry in the list (region or country), which we
                    // use as the index in the list of colors later.
                    // Also, as we are currently dealing with leaves only, the min and max
                    // are also that value.
                    double const pos = get_position( color_labels, data_col[name]);
                    edge_values[e] = { pos, 1, pos, pos };

                    check_list.insert(data_col[name]);
                }
            }

            min_value = 0;
            max_value = check_list.size() - 1;

            LOG_DBG << "check list (size=" << check_list.size() << ") = ";
            for( auto const& elem : check_list ) {
                LOG_DBG1 << elem;
            }

        } else if( is_convertible_to_double( data, i )) {
            convert_to_double( data, i );
            LOG_INFO << summarize_column( data, i );
            auto const& data_col = data[i].as<double>();

            for( size_t e = 0; e < tree.edge_count(); ++e ) {
                if( is_leaf( tree.edge_at(e)) ) {
                    auto const& name = tree.edge_at(e).secondary_node().data<CommonNodeData>().name;
                    if( !data.has_row_name( name ) ) {
                        throw std::runtime_error( "No metadata row for leaf node " + name );
                    }

                    // Get the value for that leave, and store it as the value for the edge.
                    auto const val = data_col[name];
                    edge_values[e] = { val, 1, val, val };
                    if( std::isfinite(val) ) {
                        min_value = std::min(min_value, data_col[name]);
                        max_value = std::max(max_value, data_col[name]);
                    }
                }
            }
        } else {
            // If we are here, we have a column that cannot be converted to numbers.
            // Treat it as a list of strings, where we visualize each string with its own color.
            // For this, we make a list of them, sort it, and give colors in alphabetical order.
            // In the future, we can also give colors in some other order that looks better
            // or makes more sense (country names ordered by location, for example).
            LOG_INFO << summarize_column( data, i );

            auto const& data_col = data[i].as<std::string>();

            // Make a map of all strings in the column, sorted. Then, give them their corresponding
            // index. We could use a sorted vector for this, but lookup would be slower than
            // using a map.
            std::map<std::string, size_t> value_map;
            for( auto const& v : data_col ) {
                value_map[v] = 0;
            }
            size_t cnt = 0;
            for( auto& v : value_map ) {
                color_labels.push_back( v.first );
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
        }

        write_tree(
            tree, edge_values, min_value, max_value, color_labels, color_list_nextstrain(),
            out_prefix + data[i].name() + ".svg"
        );
    }
}

void run_with_tree_labels( std::string const& tree_file, std::string const& out_prefix )
{
    // Read tree
    auto const tree = CommonTreeNewickReader().read( from_file( tree_file ));
    LOG_INFO << "Found tree with " << leaf_node_count( tree ) << " tips in tree file";

    std::vector<EdgeValues> edge_values_countries( tree.edge_count() );
    std::vector<EdgeValues> edge_values_regions( tree.edge_count() );
    std::vector<EdgeValues> edge_values_date( tree.edge_count() );
    std::vector<std::string> color_labels_countries = country_order_dimitrios;
    std::vector<std::string> color_labels_regions = region_order;
    std::vector<std::string> color_labels_date;
    std::set<std::string> check_list;

    double min_value_date = 0;
    double max_value_date = 0;

    std::map<double, size_t> date_counts;

    for( auto const& node : tree.nodes() ) {
        if( is_leaf(node) ) {
            auto const& name = node.data<CommonNodeData>().name;
            auto const parts = utils::split( name, "_" );
            // LOG_DBG << parts[0] << ":\t" << parts[1] << " (" << pos << ")" << "\t" << parts[2];

            double const pos = get_position(country_order_dimitrios, parts[1]);
            edge_values_countries[node.primary_edge().index()] = { pos, 1, pos, pos };
            check_list.insert(parts[1]);

            if( parts[1] != "ENV" && parts[1] != "MINK" ) {
                auto region = country_to_region.at(parts[1]);
                double const regpos = get_position(region_order, region);
                edge_values_regions[node.primary_edge().index()] = { regpos, 1, regpos, regpos };
            }

            auto date = stoi( parts[2] );
            if( date == 2020 ) {
                continue;
            }
            if( date > 201900 && date < 20190000 ) {
                date *= 100;
                date += 1;
            }

            auto dtb = tm_to_time( convert_to_tm( "20191201" ));
            auto dte = tm_to_time( convert_to_tm( std::to_string(date) ));
            auto diff_secs = difftime( dte, dtb );

            if( min_value_date == 0) {
                min_value_date = diff_secs;
                max_value_date = diff_secs;
            }
            if( diff_secs < min_value_date ) {
                min_value_date = diff_secs;
            }
            if( diff_secs > max_value_date ) {
                max_value_date = diff_secs;
            }

            double ddate = diff_secs;
            edge_values_date[node.primary_edge().index()] = { ddate, 1, ddate, ddate };
            date_counts[date]++;

            color_labels_date.push_back( std::to_string(date) );
        }
    }

    LOG_DBG << "min_value_date " << min_value_date << " max_value_date " << max_value_date;
    date_counts.clear();
    for( auto const& ev : edge_values_date ) {
        if( ev.sum > 0 ) {
            date_counts[ev.sum]++;
        }
    }
    for( auto const& dp : date_counts ) {
        LOG_DBG << dp.first << ": " << dp.second;
    }

    double min_value_countries = 0;
    double max_value_countries = country_order_dimitrios.size() - 1;
    // double max_value_countries = check_list.size() - 1;

    double min_value_regions = 0;
    double max_value_regions = region_order.size() - 1;
    // double max_value_regions = check_list.size() - 1;

    std::sort( color_labels_date.begin(), color_labels_date.end() );
    color_labels_date.erase( std::unique( color_labels_date.begin(), color_labels_date.end() ), color_labels_date.end() );

    write_tree(
        tree, edge_values_countries, min_value_countries, max_value_countries,
        color_labels_countries, color_list_nextstrain(), out_prefix + "_countries.svg"
    );

    write_tree(
        tree, edge_values_regions, min_value_regions, max_value_regions,
        color_labels_regions, color_list_nextstrain(6), out_prefix + "_regions.svg"
    );
    write_tree(
        tree, edge_values_date, min_value_date, max_value_date,
        color_labels_date, color_list_nextstrain(), out_prefix + "_date.svg"
    );
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

    if( meta_file != "-" ) {
        run_with_metdata( tree_file, meta_file, out_prefix );
    } else {
        run_with_tree_labels( tree_file, out_prefix );
    }

    LOG_INFO << "Finished";
    return 0;
}

/**
 * @file   test_ronex_transmission.cpp
 * @author Ugo Cupcic <ugo@shadowrobot.com>
 *
* Copyright 2011 Shadow Robot Company Ltd.
*
* This program is free software: you can redistribute it and/or modify it
* under the terms of the GNU General Public License as published by the Free
* Software Foundation, either version 2 of the License, or (at your option)
* any later version.
*
* This program is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
* more details.
*
* You should have received a copy of the GNU General Public License along
* with this program.  If not, see <http://www.gnu.org/licenses/>.
*
 * @brief Testing the ronex transmission for a given urdf.
 *
 *
 */

#include "sr_ronex_mechanism_model/ronex_transmission.hpp"
#include <sr_ronex_hardware_interface/mk2_gio_hardware_interface.hpp>
#include <ros/ros.h>
#include <pr2_mechanism_model/robot.h>
#include <gtest/gtest.h>

using namespace ronex;

TEST(RonexTransmission, constructor)
{
  //get urdf from param
  ros::NodeHandle nh;
  std::string xml_string;
  ASSERT_TRUE( nh.getParam("robot_description", xml_string) );

  TiXmlDocument urdf_xml;
  urdf_xml.Parse(xml_string.c_str());

  TiXmlElement *root = urdf_xml.FirstChildElement("robot");
  ASSERT_TRUE(root != NULL);
  pr2_hardware_interface::HardwareInterface hw;

  //add ronex
  boost::shared_ptr<ronex::GeneralIO> general_io;
  general_io.reset( new ronex::GeneralIO() );
  general_io->name_ = "ronex_12_0";
  hw.addCustomHW( general_io.get() );

  pr2_mechanism_model::Robot model(&hw);
  ASSERT_TRUE(model.initXml(root));
  pr2_mechanism_model::RobotState state(&model);
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    ros::init(argc, argv, "test_ronex_transmissions");
    ros::NodeHandle nh; // init the node
    return RUN_ALL_TESTS();
}

/* For the emacs weenies in the crowd.
   Local Variables:
   c-basic-offset: 2
   End:
*/


/**
 * @file   analogue_to_position.hpp
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
 * @brief  Contains the data mapping one pin of a GIO module to the position of the joint.
 *
 *
 */

#ifndef SR_RONEX_GENERAL_IO_POSITION_MAPPING_H_
#define SR_RONEX_GENERAL_IO_POSITION_MAPPING_H_

#include <sr_ronex_hardware_interface/mk2_gio_hardware_interface.hpp>
#include "sr_ronex_mechanism_model/mapping/ronex_mapping.hpp"

namespace ronex
{
  namespace mapping
  {
    namespace general_io
    {
      class AnalogueToPosition
        : public RonexMapping
      {
      public:
        AnalogueToPosition() {};
        AnalogueToPosition(TiXmlElement* mapping_el, pr2_mechanism_model::Robot* robot);
        virtual ~AnalogueToPosition();

        virtual void propagateFromRonex(std::vector<pr2_mechanism_model::JointState*>& js);
        virtual void propagateToRonex(std::vector<pr2_mechanism_model::JointState*>& js);

      protected:
        GeneralIO* general_io_;
        size_t pin_index_;
        bool pin_out_of_bound_;

        bool check_pin_in_bound_();
      };
    }
  }
}
/* For the emacs weenies in the crowd.
   Local Variables:
   c-basic-offset: 2
   End:
*/

#endif /* SR_RONEX_GENERAL_IO_POSITION_MAPPING_H_ */

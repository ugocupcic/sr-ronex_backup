/**
 * @file   ronex_mapping.hpp
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
 * @brief  Contains the data mapping one element of a RoNeX to a joint element.
 *
 *
 */

#ifndef _RONEX_MAPPING_H_
#define _RONEX_MAPPING_H_

#include <pr2_mechanism_model/transmission.h>

namespace ronex
{
  class RonexMapping
  {
  public:
    RonexMapping(TiXmlElement* ronex_el);
    RonexMapping(TiXmlElement* ronex_el, pr2_mechanism_model::Robot* robot);
    virtual ~RonexMapping() {};

    virtual void propagateFromRonex();
    virtual void propagateToRonex();

  protected:
    std::string ronex_id_;
  };
}

/* For the emacs weenies in the crowd.
   Local Variables:
   c-basic-offset: 2
   End:
*/

#endif /* _RONEX_MAPPING_H_ */

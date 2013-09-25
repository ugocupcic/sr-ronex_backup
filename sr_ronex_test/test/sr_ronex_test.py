#!/usr/bin/env python
# ####################################################################
# Copyright (c) 2013, Shadow Robot Company, All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.
# ####################################################################

import rospy, sys, getopt, unittest, rostest, os
import dynamic_reconfigure.client

from time import sleep
from string import Template
from threading import Lock
from sr_ronex_msgs.msg import GeneralIOState, PWM
from std_msgs.msg import Bool
from pr2_mechanism_msgs.srv import ListControllers

class EmptyTest( unittest.TestCase ):
  def test( self ):
    self.assertTrue( True )

class TestContainer( unittest.TestCase ):
  '''
  A class used to test the Shadow Robot ethercat board HW.
  
  For the test to succeed 2 ronex modules are required
  each with a stacker on it
  The digital I/O of one module should be connected to the I/O of the other
  The analogue I/O of one of the modules should be connected to a constant voltage source
  
  On each module
  12 digital inputs/outputs
  6 PWM outputs
  12 analogue inputs

  The digital inputs will read back the value we set for the outputs.
  Then all the I/O should switch roles from Input to Output and vice versa
  The PWM outputs are set to a frequency of 0.5Hz, and the digital inputs used to check the on-off period
  Six of the analogue inputs should be wired to an appropriate constant voltage source
  '''

  def setUp( self ):
    self.find_ronexes()
    self.init_clients_publishers_subscribers()
    self.state_lock = Lock()

    self.state = [ None, None ]
    self.result = False

    self.params_i = { 'input_mode_' + str( i ) : True for i in xrange( 12 ) }
    self.params_o = { 'input_mode_' + str( i ) : False for i in xrange( 12 ) }

    self.expected_analogue_values = [2928, 1432, 849, 478, 211, 91] + 6 * [0]

    self.controllers_list = [ "ronex_" + ronex_id + "_passthrough" for ronex_id in self.ronex_ids ]

  def tearDown( self ):
    pwm = PWM()
    pwm.pwm_period = 25600
    pwm.pwm_on_time_0 = 0
    pwm.pwm_on_time_1 = 0
    for p in xrange( 6 ):
      self.pwm_publishers[0][p].publish( pwm )

  def find_ronexes( self ):
    attempts = 50
    while attempts and not rospy.has_param( '/ronex/devices/0/ronex_id' ):
      if attempts == 50:
          rospy.loginfo( 'Waiting for the ronex to be loaded properly.' )
      sleep( 0.1 )
      attempts -= 1

    self.assertNotEqual( attempts, 0, 'Failed to get ronex devices from parameter server' )

    self.ronex_devs = rospy.get_param( '/ronex/devices' )
    self.assertEqual( len( self.ronex_devs ), 2, 'Error. Connect a ronex bridge with 2 ronex devices' )

  def init_clients_publishers_subscribers( self ):
    basic = '/ronex/general_io/'
    self.ronex_ids = [ self.ronex_devs[str( i )]['ronex_id'] for i in xrange( 2 ) ]
    ron = [ basic + str( id ) for id in self.ronex_ids ]

    com_dig = '/command/digital/'
    com_pwm = '/command/pwm/'
    sta = '/state'

    topics_list = rospy.get_published_topics()
    self.assertTrue( [ ron[0] + sta, 'sr_ronex_msgs/GeneralIOState' ] in topics_list )
    self.assertTrue( [ ron[1] + sta, 'sr_ronex_msgs/GeneralIOState' ] in topics_list )

    self.clients = [ dynamic_reconfigure.client.Client( r ) for r in ron ]
    self.digital_publishers = [ [ rospy.Publisher( r + com_dig + str( i ), Bool, latch = True ) for i in xrange( 12 ) ] for r in ron ]
    self.pwm_publishers = [ [ rospy.Publisher( r + com_pwm + str( i ), PWM, latch = True ) for i in xrange( 6 ) ] for r in ron ]

    self.subscriber_0 = rospy.Subscriber( ron[0] + sta, GeneralIOState, self.state_callback_0 )
    self.subscriber_1 = rospy.Subscriber( ron[1] + sta, GeneralIOState, self.state_callback_1 )


  def state_callback_0( self, msg ):
    with self.state_lock:
      self.state[0] = msg

  def state_callback_1( self, msg ):
    with self.state_lock:
      self.state[1] = msg

  def digital_test_case( self, outr, inr, message ):
    self.result = False
    self.set_ronex_io_state( outr, inr )
    for i, bool in enumerate( message ):
      self.digital_publishers[outr][i].publish( bool )
    rospy.sleep( 0.08 )

    with self.state_lock:
      self.result = ( self.state[inr].digital == message )
      self.assertTrue( self.result, 'digital i/o test failure' )

  def set_ronex_io_state( self, outr, inr ):
    self.clients[ outr ].update_configuration( self.params_o )
    self.clients[ inr ].update_configuration( self.params_i )

    rospy.sleep( 0.35 )




############################################
# TEST START
############################################

  def test_if_controllers_are_loaded( self ):
    list_controllers = rospy.ServiceProxy( 'pr2_controller_manager/list_controllers', ListControllers )
    available_controllers = list_controllers()
    for ctrl in self.controllers_list:
      self.assertTrue( ctrl in available_controllers.controllers )

  def test_change_state_one( self ):
    self.set_ronex_io_state( 0, 1 )

    config_0 = self.clients[0].get_configuration()
    config_1 = self.clients[1].get_configuration()

    for param, value in self.params_o.iteritems():
      self.assertEqual( config_0[param], value, 'Failed in first attempt to set digital I/O state' )
    for param, value in self.params_i.iteritems():
      self.assertEqual( config_1[param], value, 'Failed in first attempt to set digital I/O state' )

  def test_change_state_two( self ):
    self.set_ronex_io_state( 1, 0 )

    config_0 = self.clients[0].get_configuration()
    config_1 = self.clients[1].get_configuration()

    for param, value in self.params_i.iteritems():
      self.assertEqual( config_0[param], value, 'Failed in second attempt to set digital I/O state' )
    for param, value in self.params_o.iteritems():
      self.assertEqual( config_1[param], value, 'Failed in second attempt to set digital I/O state' )

  def test_digital_all_true( self ):
    message = 12 * [True]
    self.digital_test_case( 0, 1, message )
    self.digital_test_case( 1, 0, message )

  def test_digital_all_false( self ):
    message = 12 * [False]
    self.digital_test_case( 0, 1, message )
    self.digital_test_case( 1, 0, message )

  def test_digital_odd_true( self ):
    message = 6 * [True, False]
    self.digital_test_case( 0, 1, message )

  def test_digital_even_true( self ):
    message = 6 * [False, True]
    self.digital_test_case( 0, 1, message )

  def test_analogue( self ):
    rospy.sleep( 0.5 )
    with self.state_lock:
      result_0, result_1 = True, True
      if self.state[0].analogue[0] > 0:
        analogue = self.state[0].analogue
      else:
        analogue = self.state[1].analogue

      for ind, value in enumerate( self.expected_analogue_values ):
        self.assertAlmostEqual( value, analogue[ind], delta = 10 )

  def test_pwm_outputs( self ):

    message = 12 * [False]
    self.digital_test_case( 0, 1, message )

    params = { 'pwm_period_' + str( i ) : 25600 for i in xrange( 6 ) }
    params['pwm_clock_divider'] = 6400

    self.clients[ 0 ].update_configuration( params )
    self.clients[ 1 ].update_configuration( params )

    rospy.sleep( 0.5 )

    pwm = PWM()
    pwm.pwm_period = 25600
    pwm.pwm_on_time_0 = 30000
    pwm.pwm_on_time_1 = 30000

    self.pwm_publishers[0][0].publish( pwm )
    self.pwm_publishers[0][5].publish( pwm )

    with self.state_lock:
      self.assertFalse( self.state[1].digital[0] )
      self.assertFalse( self.state[1].digital[1] )
      self.assertFalse( self.state[1].digital[10] )
      self.assertFalse( self.state[1].digital[11] )

    rospy.sleep( 0.9 )

    with self.state_lock:
      self.assertTrue( self.state[1].digital[0] )
      self.assertTrue( self.state[1].digital[1] )
      self.assertTrue( self.state[1].digital[10] )
      self.assertTrue( self.state[1].digital[11] )

############################################
# TEST END
############################################

if __name__ == '__main__':
  do_test = os.environ.get( 'RONEX_TESTS_WITH_HARDWARE' )
  if do_test == 'yes':
    rospy.init_node( 'sr_ronex_test' )
    rostest.rosrun( 'sr_ronex_test', 'sr_ronex', TestContainer )
  else:
    rospy.init_node( 'sr_ronex_test' )
    sleep( 0.5 )
    rostest.rosrun( 'sr_ronex_test', 'sr_ronex', EmptyTest )

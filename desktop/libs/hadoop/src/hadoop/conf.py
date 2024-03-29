#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Settings to configure your Hadoop cluster."""
from desktop.lib.conf import Config, UnspecifiedConfigSection, ConfigSection
import glob
import os
import logging

HADOOP_HOME = Config(
  key="hadoop_home",
  default=os.environ.get("HADOOP_HOME", "/usr/lib/hadoop-0.20"),
  help=("Path to directory holding hadoop libs - HADOOP_HOME in " +
        "hadoop parlance; defaults to environment variable, when" +
        "set.")
)

def hadoop_bin_from_hadoop_home():
  """Returns $HADOOP_HOME/bin/hadoop-0.20"""
  return os.path.join(HADOOP_HOME.get(), "bin/hadoop")

HADOOP_BIN = Config("hadoop_bin",
  help="Path to your Hadoop binary",
  dynamic_default=hadoop_bin_from_hadoop_home,
  type=str)

# TODO(philip): This will need more love for dealing with multiple clusters.
HADOOP_CONF_DIR = Config(
  key="hadoop_conf_dir",
  default=None,
  help="If set, directory to pass to hadoop_bin (from hadoop configuration) as the --config flag.",
)

def find_jar(desired_glob, root=None):
  if root is None:
    root_f = lambda: HADOOP_HOME.get()
  else:
    root_f = lambda: root
  def f():
    pattern = os.path.join(root_f(), desired_glob)
    possibilities = glob.glob(pattern)
    if len(possibilities) == 1:
      return possibilities[0]
    elif len(possibilities) >= 1:
      logging.warning("Found multiple jars matching %s: %s" % (pattern, possibilities))
      return None
    else:
      logging.warning("Trouble finding jars matching %s" % (pattern,))
      return None
  if root is None:
    root_str = "$HADOOP_HOME"
  else:
    root_str = root
  f.__doc__ = "Finds %s/%s" % (root_str, desired_glob)
  return f

def find_examples_jar():
  """
  Finds $HADOOP_HOME/hadoop-*examples*.jar
  """
  return find_jar("hadoop-*examples*.jar")

HADOOP_EXAMPLES_JAR = Config(
  key="hadoop_examples_jar",
  dynamic_default=find_examples_jar(),
  help="Path to the hadoop-examples.jar (used for tests and jobdesigner setup)",
  type=str,
  private=True)

HADOOP_STREAMING_JAR = Config(
  key="hadoop_examples_jar",
  dynamic_default=find_jar(os.path.join("contrib", "streaming", "hadoop-*streaming*.jar")),
  help="Path to the hadoop-streaming.jar (used by jobdesigner)",
  type=str,
  private=True)

HADOOP_TEST_JAR = Config("hadoop_test_jar",
  help="[Used by testing code.] Path to hadoop-test.jar",
  dynamic_default=find_jar("hadoop-*test*.jar"),
  type=str,
  private=True)

HADOOP_PLUGIN_CLASSPATH = Config("hadoop_plugin_classpath",
  help="[Used only in testing code.] Path to the Hadoop plugin jar.",
  type=str,
  dynamic_default=find_jar("../../java-lib/hue-plugins-*.jar", root=os.path.dirname(__file__)),
  private=True)

HDFS_CLUSTERS = UnspecifiedConfigSection(
  "hdfs_clusters",
  help="One entry for each HDFS cluster",
  each=ConfigSection(
    help="Information about a single HDFS cluster",
    members=dict(
      NN_HOST=Config("namenode_host", help="IP for name node"),
      NN_THRIFT_PORT=Config("thrift_port", help="Thrift port for name node", default=9090,
                            type=int),
      NN_HDFS_PORT=Config("hdfs_port", help="Hadoop IPC port for the name node", default=8020,
                            type=int)
    )
  )
)

MR_CLUSTERS = UnspecifiedConfigSection(
  "mapred_clusters",
  help="One entry for each MapReduce cluster",
  each=ConfigSection(
    help="Information about a single MapReduce cluster",
    members=dict(
      JT_HOST=Config("jobtracker_host", help="IP for JobTracker"),
      JT_THRIFT_PORT=Config("thrift_port", help="Thrift port for JobTracker", default=9290,
                            type=int))))

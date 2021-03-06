/**
 * Autogenerated by Thrift
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 */
package com.cloudera.beeswax.api;


import java.util.Set;
import java.util.HashSet;
import java.util.Collections;
import org.apache.thrift.IntRangeSet;
import java.util.Map;
import java.util.HashMap;

public class FileResourceType {
  public static final int JAR = 0;
  public static final int ARCHIVE = 1;
  public static final int FILE = 2;

  public static final IntRangeSet VALID_VALUES = new IntRangeSet(
    JAR, 
    ARCHIVE, 
    FILE );

  public static final Map<Integer, String> VALUES_TO_NAMES = new HashMap<Integer, String>() {{
    put(JAR, "JAR");
    put(ARCHIVE, "ARCHIVE");
    put(FILE, "FILE");
  }};
}

package org.renpy.android;

import android.content.Context;
import android.os.Vibrator;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

/**
 * Methods that are expected to be called via JNI, to access the
 * device's non-screen hardware. (For example, the vibration and
 * accelerometer.)
 */
 public class Hardware {
     
     // The context.
     static Context context;
     
     /**
      * Vibrate for s seconds.
      */
     static void vibrate(double s) {
         Vibrator v = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
         if (v != null) {
             v.vibrate((int) (1000 * s));
         }
     }

     static SensorEvent lastEvent = null;
     
     static class AccelListener implements SensorEventListener {
         public void onSensorChanged(SensorEvent ev) {
             lastEvent = ev;
         }

         public void onAccuracyChanged(Sensor sensor , int accuracy) {
         }

     }

     static AccelListener accelListener = new AccelListener();
     
     /**
      * Enable or Disable the accelerometer.
      */
     static void accelerometerEnable(boolean enable) {
         SensorManager sm = (SensorManager) context.getSystemService(Context.SENSOR_SERVICE);
         Sensor accel = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

         if (accel == null) {
             return;
         }
         
         if (enable) {
             sm.registerListener(accelListener, accel, SensorManager.SENSOR_DELAY_GAME);             
         } else {
             sm.unregisterListener(accelListener, accel);
         
         }
     }
     
 
     static float[] accelerometerReading() {
         if (lastEvent != null) {
             return lastEvent.values;
         } else {
             float rv[] = { 0f, 0f, 0f };
             return rv;
         }
     }
         

}
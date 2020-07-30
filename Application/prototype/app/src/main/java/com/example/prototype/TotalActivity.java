package com.example.prototype;

import androidx.appcompat.app.AppCompatActivity;


import android.os.Bundle;
import android.widget.Button;
import android.content.Intent;
import android.view.View;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Button;
import android.content.Intent;
import android.view.View;
import android.widget.EditText;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SimpleAdapter;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;

import java.io.InputStream;
import java.io.InputStreamReader;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;

public class TotalActivity extends Activity {


    String myJSON;

    private static final String TAG_RESULTS = "result";
    private static final String TAG_S3 = "S3";
    private static final String TAG_S4 = "S4";
    private static final String TAG_BPM = "BPM";
    private static final String TAG_disease = "disease";
    private static final String TAG_time = "time";
    private static final String TAG_heartage = "heartage";

    JSONArray vital = null;

    ArrayList<HashMap<String, String>> vitalSign;

    ListView list;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_total);
        list = (ListView) findViewById(R.id.ListVeiw);
        vitalSign = new ArrayList<HashMap<String, String>>();
        getData("http://10.0.2.2/PHP_connection.php");//ip에 따라 바꿀 예정
    }
        protected void showList() {
            try {
                JSONObject jsonObj = new JSONObject(myJSON);
                vital = jsonObj.getJSONArray(TAG_RESULTS);

                for (int i = 0; i < vital.length(); i++) {
                    JSONObject c = vital.getJSONObject(i);
                    String S3 = c.getString(TAG_S3);
                    String S4 = c.getString(TAG_S4);
                    String BPM = c.getString(TAG_BPM);
                    String disease = c.getString(TAG_disease);
                    String time = c.getString(TAG_time);
                    String heartage = c.getString(TAG_heartage);

                    HashMap<String, String> persons = new HashMap<String, String>();


                    persons.put(TAG_S3, S3);
                    persons.put(TAG_S4, S4);
                    persons.put(TAG_BPM, BPM);
                    persons.put(TAG_disease, disease);
                    persons.put(TAG_time, time);
                    persons.put(TAG_heartage,heartage);

                    vitalSign.add(persons);
                }

                ListAdapter adapter = new SimpleAdapter(
                        TotalActivity.this, vitalSign, R.layout.list_item,
                        new String[]{TAG_S3, TAG_S4, TAG_BPM, TAG_disease, TAG_time, TAG_heartage},
                        new int[]{R.id.S3, R.id.S4, R.id.BPM, R.id.disease, R.id.time,R.id.heartage}
                );

                list.setAdapter(adapter);

            } catch (JSONException e) {
                e.printStackTrace();
            }

        }

        public void getData (String url){
            class GetDataJSON extends AsyncTask<String, Void, String> {

                @Override
                protected String doInBackground(String... params) {

                    String uri = params[0];

                    BufferedReader bufferedReader = null;
                    try {
                        URL url = new URL(uri);
                        HttpURLConnection con = (HttpURLConnection) url.openConnection();
                        StringBuilder sb = new StringBuilder();

                        bufferedReader = new BufferedReader(new InputStreamReader(con.getInputStream()));

                        String json;
                        while ((json = bufferedReader.readLine()) != null) {
                            sb.append(json + "\n");
                        }

                        return sb.toString().trim();

                    } catch (Exception e) {
                        return null;
                    }


                }

                @Override
                protected void onPostExecute(String result) {
                    myJSON = result;
                    showList();
                }
            }
            GetDataJSON g = new GetDataJSON();
            g.execute(url);
        }


    }




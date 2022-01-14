package com.example.slelatex;

import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import java.io.IOException;

public class Application extends javafx.application.Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(Application.class.getResource("main.fxml"));
        stage.getIcons().add(new Image(Application.class.getResourceAsStream("img/icon.jpg")));
        Scene scene = new Scene(fxmlLoader.load(), 1000, 600);
        stage.setTitle("Random Unimodular SLE Solver");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) throws IOException {
        launch();
    }
}
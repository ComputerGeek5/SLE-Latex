package com.example.slelatex;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.stage.Stage;


import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

public class MainController {
    @FXML
    private TextField numberOfSolutionsField;

    @FXML
    private TextArea solution;

    @FXML
    protected void solveSystem() {
        String numberOfSolutions = numberOfSolutionsField.getText();
        try {
            executePythonScript(numberOfSolutions);
            convertLatexToPDF();
            openPDF();
        } catch (Exception e) {
            e.printStackTrace();
            solution.setStyle("-fx-text-fill: #ff0000;");
            solution.setText("Could not solve random matrix. Something went wrong!");
        }
    }

    private void executePythonScript(String numberOfSolutions) throws IOException {
        String scriptLocation = System.getProperty("user.dir") + "\\System_of_Linear_Equations.py";
        ProcessBuilder executeScript = new ProcessBuilder(
                "python",
                scriptLocation,
                numberOfSolutions
        );
        Process process = executeScript.start();

        BufferedReader processError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

        String errorLine;
        while ((errorLine = processError.readLine()) != null) {
            System.out.println(errorLine);
        }

        BufferedReader processOutput = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String outputLine, result = "";
        while ((outputLine = processOutput.readLine()) != null) {
            result += outputLine;
        }

        solution.setText(result);
    }

    private void convertLatexToPDF() throws IOException {
        String texCommand = "C:\\Users\\Erart\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\pdflatex.exe";
        String texLocation = System.getProperty("user.dir") + "\\Matrix.tex";
        ProcessBuilder convertToLatex = new ProcessBuilder(
                texCommand,
                texLocation
        );

        boolean texExists = new File(texLocation).exists();
        if (texExists) {
            convertToLatex.start();
        }
    }

    private void openPDF() throws IOException {
        String pdfLocation = System.getProperty("user.dir") + "\\Matrix.pdf";
        File pdfFile = new File(pdfLocation);

        boolean pdfExists = pdfFile.exists();
        if (pdfExists) {
            Desktop.getDesktop().open(pdfFile);
        }
    }


    public void open(ActionEvent event) throws IOException {
        try {
            openPDF();
        } catch (IOException e) {
            e.printStackTrace();
            solution.setStyle("-fx-text-fill: #ff0000;");
            solution.setText("Could open solution. Something went wrong!");
        }
    }


    public void exit(ActionEvent event) {
        Stage stage = (Stage)((Node) event.getSource()).getScene().getWindow();
        stage.close();
        System.exit(0);
    }
}
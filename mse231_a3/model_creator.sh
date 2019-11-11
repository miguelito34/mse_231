echo "Teaching model $1"
echo ""

cat training_data.tsv | python3 vw_format_m$1.py > vw_training_data.txt
cat test_data.tsv | python3 vw_format_m$1.py > vw_test_data.txt


echo ""
echo "Training model $1..."
echo ""
vw -d vw_training_data.txt -f predictor.vw --loss_function logistic --cubic sss -q sc --ngram t2

echo ""
echo "Creating predictions on training set..."
echo ""
vw -d vw_training_data.txt -t -i predictor.vw -p training_predictions.txt --link=logistic

echo ""
echo "Creating predictions on test set..."
echo ""
vw -d vw_test_data.txt -t -i predictor.vw -p test_predictions.txt --link=logistic

echo ""
echo "Here's information about model $1 features:"
echo "MASKED: vw-varinfo --loss_function logistic vw_training_data.txt"
echo ""

echo ""
echo "Evaluating model $1"
echo ""
Rscript model_evaluation.R

echo ""
echo "If you're interested in seeing AUC and Calibration plots, open the ""Rplots.pdf"" file"
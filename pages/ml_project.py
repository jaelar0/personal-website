import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import time
from settings import ml_methods_cr_intro, ml_methods_part1

dash.register_page(__name__, path='/ml-project')

layout =  html.Div([
            html.H1(['Borrower Credit Risk using Machine Learning'], id="ml-methods-cr"),
            html.Br(),
            html.P(["Link to Github for Code:", html.A("Github Page", href="https://github.com/jaelar0/ml_credit_project/blob/master/final_project.ipynb", style={"font-family": "lightFont", "color": "white"}),]),
            html.Br(),
            html.P(ml_methods_cr_intro),
            html.Br(),
            html.H3(['Preprocessing Data']),
            html.P(ml_methods_part1),
            html.Br(),
            html.H3(['Feature Engineering']),
            html.P("In this section, we renamed fields into something more meaningful, extrapolated fields from other fields,\
                   and grouped categorical fields in a way that reduces dimensionality. \
                   The final result is a dataframe, named encode_df in the code, with our target variable, aka. class variable, \
                   named 'bad_ind' and our set of features we wish to train our model on."),
            html.Br(),
            html.P("Next, we conducted EDA on some of our features. The goal was to \
                identify relationships between our features and their distributions. \
                As we can see from the picture on the right, not a whole lot \
                can be derived in terms of classifying/clustering our population groups."
            ),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                    'backgroundColor': 'black', 
                                                    "borderRadius": "10px",
                                                    'justifyContent': 'center',
                                                    'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_eda.png?{time.time()}', 
                className='ml-method-eda',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.P("This simple correlation matrix highlights two things. \
                               First, no feature seems to have a strong relationship with the target \
                               variable. Second, this further reinforces our initial inclination \
                               that the target variable in our data is highly imbalanced (ie. not enough 'bad' borrowers)."
            ),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                    'backgroundColor': 'black', 
                                                    "borderRadius": "10px",
                                                    'justifyContent': 'center',
                                                    'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_corr.png?{time.time()}', 
                className='ml-method-eda',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.H3(['Classifying Bad Borrowers - Logistic Regression']),
            html.P("As previously mentioned, we will need to deal with our imbalanced dataset before training any model. Because we have a low number of 'bad' borrowers in our dataset, \
                   it would be nearly impossible to train an accurate model that can predict a borrowers class if nothing is done to the dataset. \
                   This problem introduced us to data sampling algorithms that approach this issue differently ranging from undersampling the majority class, \
                   oversampling minority class, and a hybrid randomized approach. Among the many oversampling techniques available, \
                   we chose an oversampling technique called Synthetic Minority Over-sampling Technique (SMOTE). This technique generates synthetic data points \
                   between each sample point of the minority class and its k nearest neighbor. See below for a great graphic on this process. \
                   Essentially, we are running a knn algorithm on each data point in the \
                   minority class. This technique was chosen primarily for its simplicity and usability in the financial services industry. \
                   Once our dataset was balanced, we were able to normalize our fields and perform train-test splits before sending it off to our models. \
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                    'backgroundColor': 'black', 
                                                    "borderRadius": "10px",
                                                    'justifyContent': 'center',
                                                    'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_smote.png?{time.time()}', 
                className='ml-method-center',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.Br(),        
            html.P("Although our simple LR model performed relatively well, by looking at the confusion matrix, the False Negative number (Actual Bad, Predicted Good) for our Bad Borrower target class is hard to miss.\
                    We can see the same story in our Recall score for Bad Borrowers from the table, which is the worst performing of all performance factors (.79). \
                    Another thing to note is that our k-fold cross validation also shows that this model generalizes well and performs the \
                    same across our subsets (k=5). Overall, the model performed well as seen from the metrics, but it did leave more to be desired.\
                    "),
            html.Br(), 
            html.Div(className="rf-classifier-results", style={'display': 'flex', 'backgroundColor': 'black', "borderRadius": "10px"}, children=[
                html.Img(src=f'/assets/ml_credit_results.png?{time.time()}', 
                        className='ml-method-min', 
                        style={'flex': '1',
                                'display': 'flex',
                                'width': '40%',
                                'height': '60%',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'padding': '10px'}
                ),
                html.Img(src=f'/assets/ml_credit_roc.png?{time.time()}', 
                        className='ml-method-eda', 
                        style={'flex': '1',
                            'width': '40%',
                            'height': '60%',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '10px'
                            }
                )
            ]),          
            html.P("Another important concept when it comes to classification models is that of feature importance. \
            What the bar chart is showing is that occupation and education features contribute more to the \
            model's predictions. There is reason to believe there is high multicollinearity as a result of our one-hot encoding.\
            In the future, we could either remove these features or engineer the features in a way that captures as much information \
            as possible into a single column.\
            "),   
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                'backgroundColor': 'black', 
                "borderRadius": "10px",
                'justifyContent': 'center',
                'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_fi.png?{time.time()}', className='ml-method-min', 
                    style={'display': 'flex',
                        'width': '50%',
                        'height': '50%',
                        'justifyContent': 'center',
                        'padding': '10px'})
            ]),
            html.Br(),
            html.H3(['Classifying Bad Borrowers - Random Forest Classifier']),
            html.P("We suspected multicollinearity in the previous example and as a result, the LR model was relying too heavily on those features.\
                   This is the main reason why Random Forest was chosen as the next model to test. \
                   This model uses Bagging to reduce variance and train on random subsets of the data. Because of this, we do not rely on any single feature \
                   and we end up with a more generalized model. This can further be seen below by the cross-validation scores and robustness across \
                   the metrics.\
                   "),
            html.Br(),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 'backgroundColor': 'black', "borderRadius": "10px"}, children=[
                html.Img(src=f'/assets/ml_credit_rf_results.png?{time.time()}', 
                        className='ml-method-min', 
                        style={'flex': '1',
                                'display': 'flex',
                                'width': '50%',
                                'height': '70%',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'padding': '10px'}
                ),
                html.Img(src=f'/assets/ml_credit_rf_roc.png?{time.time()}', 
                        className='ml-method-eda', 
                        style={'flex': '1.2',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'padding': '10px'
                            }
                )
            ]),
            html.Br(),        
            html.P("The feature importance scores are more intuitive and align with what we would think determines 'bad' borrower."),   
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                            'backgroundColor': 'black', 
                                                            "borderRadius": "10px",
                                                            'justifyContent': 'center',
                                                            'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_rf_fi.png?{time.time()}', 
                        className='ml-method-eda',
                        style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.H3(['Survival Analysis - Vintage Analysis']),
            html.P("This section attempts to explain the time component of identifying 'bad' borrowers with the use of statistical models. \
                   Below is the result of grouping the loans \
                   by their origination date and analyzing the amount of 'bad' loans over time as loan groups approach maturity. \
                   As expected, there is a positive relationship between loan term and amount of 'bad' loans for a given portfolio. \
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                            'backgroundColor': 'black', 
                                                            "borderRadius": "10px",
                                                            'justifyContent': 'center',
                                                            'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/surv_analysis.png?{time.time()}', 
                        className='ml-method-surv',
                        style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.Br(),
            html.H3(['Survival Analysis - Kaplan-Meier']),
            html.P("A simple Kaplan-Meier statistical model was also ran with the same goal as the vintage analysis. \
                   This time, no grouping is done and \
                   the outputs are a set of confidence interval probability estimates of a loan remaining 'good' throughout its lifetime. \
                   The blue solid line represents the actual distribution of 'good' loans throughout time for our dataset. \
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                                'backgroundColor': 'black', 
                                                "borderRadius": "10px",
                                                'justifyContent': 'center',
                                                'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/km_surv_analysis.png?{time.time()}', 
                className='ml-method-surv',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.H3(['Survival Analysis - Cox Proportional Hazard Model']),
            html.P("Expanding on the Kaplan-Meier model, we wanted to understand the effect different variables (features) have on the time-until-the-event. \
                    The highly imbalanced target class became an issue once again when training this model. Unlike before, we cannot simmply use things like \
                   SMOTE or other oversampling/undersampling techniques (We actually did use SMOTE in a trial run but the results were deleted from the code due to inaccuracies.).\
                   We used L2 Regularization, which is a technique aimed at handling all types of issues including imbalanced data. It works by penalizing the model's loss \
                   function therefore preventing dominant classes (ie. 'good' borrowers) from overpowering the model. \
                   Using this technique, as well as adjusting hyperparameters,we did not achieve our lofty goal of 70% accuracy score (fell just short - 68%). \
                   Our accuracy score is just 18 points better than a random model, but at least we know there were steps taken to try to squeeze out prediction power. \
                   Another takeaway is that\
                   this model gives us a good idea of what variables are most important in explaining the time component of loans turning 'bad'.\
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                    'backgroundColor': 'black', 
                                    "borderRadius": "10px",
                                    'justifyContent': 'center',
                                    'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_chp_score.png?{time.time()}', 
                className='ml-method-chp',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),    
            html.P("Another thing we can see from this experiment is that we can look the estimated predictions. \
                Of particular importance, are the records the model predicted as having a probability of staying 'good' less than 90%. \
                All but one of these records, did actually turn 'bad' and that conversion happened early. \
                This explains why the probability curves have an aggressive negative slope \
                since these loans actually have a probability of 'good' equal to zero after their early conversion. \
                We should note that , as the code states, we only have 80 total \
                'bad' loans in our testing data. Check code for more details. \
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                'backgroundColor': 'black', 
                                "borderRadius": "10px",
                                'justifyContent': 'center',
                                'alignItems': 'center'}, children=[
            html.Img(src=f'/assets/ml_credit_90_chp.png?{time.time()}', 
            className='ml-method-min',
            style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),    
            html.P("One last thing we can do with this model is to get probabilities using new synthetic data. \
                Four records were created to analyize probabilities and essentially, to spit out PDs. \
                This also shows that the model is highly favoring the 'years employed' variable. The data record with the highest \
                income out of the 4 \
                was intentionally given a low 'years employed' variable which resulted in a higher PD than all (Sample 3 in chart). \
            "),
            html.Div(className="rf-classifier-results", style={'display': 'flex', 
                                    'backgroundColor': 'black', 
                                    "borderRadius": "10px",
                                    'justifyContent': 'center',
                                    'alignItems': 'center'}, children=[
                html.Img(src=f'/assets/ml_credit_chp_preds.png?{time.time()}', 
                className='ml-method-min',
                style={'maxWidth': '60%', 'height': '60%', 'padding': '20px'})
            ]),
            html.Br(),
            html.Br(),
            html.H3(['Final Thoughts']),
            html.Br(),
            html.H4(['Application']),
            html.P("An important question still remains. How can we use these learnings to create a loan approval system? \
                   The prevailing idea is to use the classification model findings to create a risk rating scorecard and then the survival analysis \
                   to hand out PDs for the borrowers. Vintage analysis can also be used to measure 'bad' borrower levels across the portfolio. \
            "),
            html.Br(),
            html.H4(['Limitations']),
            html.P("The data lacks relevant data such as credit scores which are widely used in the industry. \
                   Actual dates, such as origination date instead of number of months, are missing and could have been used to link to \
                   external events (ie COVID, 2007 crisis). \
                   The validity of the research can come into play since we do not exactly know the source of the data. \
                   Perhaps the data does not align well with reality or current customer behavior.\
            "),
            html.Br(),
            html.H4(['Future Work']),
            html.P("Classification model choice is an area we can improve on as we chose interpretability over prediction-power, this is \
                   especially true for the logistic regression. \
                   Survival Analysis, like most statistical concepts, is a very nuanced subject and we were not able to experiment with more \
                   due to the fact that it is out of the scope of the course (and education). There are also new techniques that blend SA with machine learning or \
                   deep learning algorithms. \
            "),
        ])


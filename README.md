# ElectionTest
This project is an end-to-end Election Analytics and Prediction System designed to demonstrate how machine learning, historical election data, and social media indicators can be combined into a unified decision-support platform. The system is built as a full-stack application with a Python-based backend and a browser-based frontend, focusing on constituency-level election analysis and parliamentary outcome simulation rather than claiming real-world election forecasting accuracy.

The backend is implemented using FastAPI and is responsible for data ingestion, preprocessing, model training, prediction, explainability, and report generation. Users can upload election history data and social media influence data in CSV format through defined API endpoints. These datasets are merged and processed to generate features such as vote share, engagement metrics, and sentiment indicators. A supervised machine learning model is trained on the processed data to estimate candidate win probabilities. Model accuracy is calculated on available data to provide transparency into performance.

In addition to candidate-level predictions, the system includes parliamentary aggregation logic. Constituency-level results are aggregated to simulate seat distribution across political parties, and a Prime Minister prediction is derived based on majority rules. This allows the platform to demonstrate higher-level reasoning beyond individual predictions, reflecting how national leadership outcomes emerge from local elections.

To improve transparency and interpretability, the project integrates SHAP-based explainability. Feature importance visualizations are generated to show how different factors influence predictions. Automated PDF reports are produced containing charts, summaries, and analytical results, enabling offline review and presentation.

The frontend is implemented using HTML, CSS, and JavaScript and communicates with the backend through REST APIs. It provides a structured dashboard interface inspired by government analytics portals, supporting CSV uploads, prediction execution, visualization through charts, accuracy display, and report downloads. The interface supports both English and Nepali language presentation to improve accessibility.

This project is intended as an academic and portfolio demonstration of applied machine learning, data engineering, and full-stack development. It emphasizes system design, explainability, and analytical reasoning rather than real-world political prediction, making it suitable for educational evaluation, technical interviews, and further research experimentation.
#Outputs/Ui
<img width="1916" height="821" alt="Screenshot 2026-02-09 214659" src="https://github.com/user-attachments/assets/e83ec1a4-f522-43b8-a0f6-da68c62f1594" />
<img width="1913" height="824" alt="Screenshot 2026-02-09 214733" src="https://github.com/user-attachments/assets/98973e42-1418-4bdc-8c52-41e6d23c997a" />
<img width="1919" height="783" alt="Screenshot 2026-02-09 214749" src="https://github.com/user-attachments/assets/4eded4d4-bacf-4e8a-bcac-d38c8df3732a" />
<img width="1397" height="604" alt="Screenshot 2026-02-09 214811" src="https://github.com/user-attachments/assets/470f8693-a73e-4ed6-8dba-eafb433bcf58" />

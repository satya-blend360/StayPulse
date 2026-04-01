import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from jinja2 import Environment, FileSystemLoader
from mapping import add_scale_info
import base64
from io import BytesIO

from ai_engine import StayPulseAIEngine

class StayPulseReportEngine:
    def __init__(self, data_path='final_data.csv'):
        print("Loading and preparing data...")
        self.df = pd.read_csv(data_path)
        self.df = add_scale_info(self.df)
        self.output_dir = 'reports'
        self.ai_engine = None
        try:
            self.ai_engine = StayPulseAIEngine()
        except Exception as e:
            print(f"Skipping AI: {e}")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'images'), exist_ok=True)

    def _get_kpis(self, data):
        return {
            'nps': round(data['nps_score'].mean(), 1),
            'osat': round(data['osat_score'].mean(), 1),
            'responses': len(data)
        }

    def _get_problem_impact(self, data):
        # Filter rows with problem info
        prob_data = data[data['problem_experienced'].notnull()]
        if prob_data.empty: return None
        
        rate = round(prob_data['problem_experienced'].mean() * 100, 1)
        nps_with = round(prob_data[prob_data['problem_experienced'] == True]['nps_score'].mean(), 1)
        nps_without = round(prob_data[prob_data['problem_experienced'] == False]['nps_score'].mean(), 1)
        
        return {
            'rate': rate,
            'nps_with_problem': nps_with,
            'nps_without_problem': nps_without,
            'potential_gain': round(nps_without - nps_with, 1)
        }

    def _generate_drivers_chart(self, data, name):
        cols = [
            'osat_service_score', 'osat_cleanliness_score', 
            'osat_guestroom_score', 'osat_checkin_score', 
            'osat_checkout_score', 'osat_internet_score'
        ]
        labels = ['Service', 'Clean', 'Room', 'Check-in', 'Check-out', 'WiFi']
        
        scores = data[cols].mean()
        
        plt.figure(figsize=(8, 4))
        plt.bar(labels, scores, color='#005195')
        plt.ylim(0, 10)
        plt.title(f"{name} Satisfaction Drivers")
        plt.ylabel("Avg Score")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Save to buffer for base64
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        
        # Convert to base64
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    def generate_report(self, filter_type='brand', filter_value='DAYS INN'):
        """
        filter_type: 'brand' or 'scale'
        filter_value: e.g. 'DAYS INN' or 'Economy'
        """
        name = filter_value
        if filter_type == 'brand':
            data = self.df[self.df['property_brand_name'] == filter_value.upper()]
        else:
            data = self.df[self.df['chain_scale'] == filter_value]

        if data.empty:
            print(f"No data found for {filter_type}: {filter_value}")
            return

        print(f"Generating report for {name}...")
        
        # 1. Calculate Metrics
        kpis = self._get_kpis(data)
        prob_impact = self._get_problem_impact(data)
        
        # 2. Top States
        top_states_raw = data.groupby('property_state_code').agg(
            nps=('nps_score', 'mean'),
            osat=('osat_score', 'mean'),
            responses=('nps_score', 'count')
        ).sort_values('nps', ascending=False).head(5)
        
        top_states = []
        for state, row in top_states_raw.iterrows():
            top_states.append({
                'name': state,
                'nps': round(row['nps'], 1),
                'osat': round(row['osat'], 1),
                'responses': int(row['responses'])
            })

        # 2.5 Voice of Customer (Comments)
        comments_data = data[data['main_comment'].notnull()]
        positive_comments = comments_data[comments_data['nps_score'] >= 9]['main_comment'].head(3).tolist()
        negative_comments = comments_data[comments_data['nps_score'] <= 4]['main_comment'].head(3).tolist()

        # 2.7 AI Insights
        ai_insights = None
        if self.ai_engine:
            print("Fetching AI Insights...")
            sample_comments = comments_data['main_comment'].head(50).tolist()
            ai_insights = self.ai_engine.get_executive_insights(name, kpis, prob_impact, sample_comments)

        # 3. Generate Visuals
        chart_path = self._generate_drivers_chart(data, name)

        # 4. Render HTML
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('templates/report_template.html')
        
        html_out = template.render(
            title=name,
            period="Monthly Summary (April 2026)",
            kpis=kpis,
            problem_impact=prob_impact,
            top_states=top_states,
            positive_comments=positive_comments,
            negative_comments=negative_comments,
            ai_insights=ai_insights,
            chart_path=chart_path 
        )
        
        out_file = os.path.join(self.output_dir, f"{name.replace(' ', '_').lower()}_report.html")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(html_out)
        
        print(f"Report saved to: {out_file}")

if __name__ == "__main__":
    import sys
    engine = StayPulseReportEngine()
    
    if len(sys.argv) > 2:
        f_type = sys.argv[1].lower() # 'brand' or 'scale'
        f_value = sys.argv[2]        # e.g. 'SUPER 8'
        engine.generate_report(filter_type=f_type, filter_value=f_value)
    else:
        print("\nUsage: python report_engine.py [type] [value]")
        print("Example: python report_engine.py brand \"SUPER 8\"")
        print("Example: python report_engine.py scale \"Economy\"")
        
        # Default run if no args
        print("\n--- Running default test reports ---")
        engine.generate_report(filter_type='brand', filter_value='DAYS INN')
        engine.generate_report(filter_type='scale', filter_value='Economy')

# Screenshots

Place the following screenshots in this folder once the app is running:

- dashboard.png - main Streamlit landing view
- upload.png - outfit upload tab
- recommendations.png - recommendation results with score components
- analytics.png - beta-simulation metrics dashboard

Quick way to generate blank placeholders:

```bash
python -c "from PIL import Image; [Image.new('RGB',(1280,720),'#1f2a44').save(f'screenshots/{n}.png') for n in ['dashboard','upload','recommendations','analytics']]"
```

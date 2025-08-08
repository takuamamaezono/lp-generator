# 🚀 LP Rough Draft Auto Generator

Automatically generate LP (Landing Page) rough drafts from specification CSV files and upload to Docbase.

[🇯🇵 日本語](README_JP.md)

## ✨ Features

- **Automatic Generation**: CSV specification → Complete LP rough draft
- **Product Information Extraction**: SKU/JAN codes, specifications, selling points
- **Docbase Integration**: Auto-upload generated drafts
- **Docker Support**: Easy team deployment
- **Production Ready**: Tested with real product data

## 📦 What's Generated

- **LP Rough Draft** (10-page structure)
- **Product Information** (Name, SKU/JAN, specifications)
- **Marketing Copy** (Based on specification selling points)

## 🎯 Demo

### Input: Specification CSV
```csv
商品名,PowerArQ Electric Blanket Lite
JANコード（バリエーション別）,ブラック：4571427130640
,ベージュ：4571427130657
セールスポイント,●10段階の温度調節
,●過熱保護システム搭載
```

### Output: Complete LP Draft
✅ **Live Example**: [PowerArQ Electric Blanket Lite LP Draft](https://go.docbase.io/posts/3891342)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/lp-generator.git
cd lp-generator

# Setup environment
cp .env.example .env
# Edit .env with your Docbase API token

# Start system
docker-compose up -d

# Generate LP draft
docker-compose exec lp-generator python correct_lp_generator.py /app/data/specification.csv --upload
```

### Option 2: Local Environment

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/lp-generator.git
cd lp-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_pdf.txt

# Generate LP draft
python correct_lp_generator.py specification.csv --upload
```

## 📋 Requirements

### System Requirements
- Docker & Docker Compose (recommended)
- OR Python 3.11+ with pip

### Input Requirements
- **Specification CSV file** with product details
- **Docbase API token** for upload functionality

### CSV Format
The system expects Japanese specification CSV files with these fields:
- `商品名`: Product name
- `商品名カナ`: Product name in katakana
- `メーカー型番`: Model number
- `JANコード（バリエーション別）`: JAN codes by variant
- `セールスポイント`: Selling points (●-prefixed list)

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```bash
DOCBASE_ACCESS_TOKEN=your_docbase_token
DOCBASE_TEAM=your_team_name
```

### Docbase API Token
1. Go to Docbase → Settings → API
2. Generate new token
3. Add to `.env` file

## 📖 Usage

### Basic Commands

```bash
# Generate only (no upload)
python correct_lp_generator.py specification.csv

# Generate and upload to Docbase
python correct_lp_generator.py specification.csv --upload

# Docker version
docker-compose exec lp-generator python correct_lp_generator.py /app/data/specification.csv --upload
```

### File Structure
```
lp-generator/
├── data/                # Input CSV files
├── output/              # Generated LP drafts
├── templates/           # Template files
├── correct_lp_generator.py  # Main generator
├── docbase_lp_uploader.py   # Docbase integration
├── docker-compose.yml   # Docker configuration
└── README.md           # This file
```

## 🎨 Generated LP Structure

### 10-Page Layout
1. **TOP Catch**: Product name & key features
2. **Sales Record**: Brand credibility & achievements
3. **Brand Value**: Brand story & safety
4. **Main Feature 1**: Primary functionality
5. **Main Feature 2**: Secondary functionality
6. **Usage Scenes**: Lifestyle integration
7. **Specifications**: Technical details
8. **Accessories**: Included items
9. **Warranty**: After-sales support
10. **FAQ**: Common questions

### Page Components
- **Layout Guide**: Design instructions
- **Text Content**: Marketing copy
- **Image Notes**: Photography requirements

## 🔍 Examples

### PowerArQ Electric Blanket Lite
- **Input**: [Specification CSV](data/sample_specification.csv)
- **Output**: [Generated LP Draft](https://go.docbase.io/posts/3891342)
- **Features**: 10-level temperature control, overheat protection, camping-friendly design

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/YOUR_USERNAME/lp-generator.git
cd lp-generator

# Create development environment
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r requirements_pdf.txt
```

### Testing
```bash
# Test with sample data
python correct_lp_generator.py data/sample_specification.csv

# Test Docker environment
docker-compose exec lp-generator python correct_lp_generator.py /app/data/sample_specification.csv
```

## 📊 Roadmap

- [ ] Excel specification file support
- [ ] PDF press release processing
- [ ] Multi-language support
- [ ] Layout design automation
- [ ] Image integration
- [ ] API endpoint for web integration

## 🐛 Troubleshooting

### Common Issues

**Container won't start**
```bash
docker-compose logs
docker-compose build --no-cache
```

**API errors**
- Check `.env` file configuration
- Verify Docbase API token permissions

**File not found**
- Ensure files are in `data/` directory
- Check file path and permissions

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/lp-generator/issues)
- **Documentation**: [Wiki](https://github.com/YOUR_USERNAME/lp-generator/wiki)
- **Examples**: [Examples Directory](examples/)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for efficient LP production workflow
- Tested with real product specifications
- Optimized for Japanese market requirements

---

**Made with ❤️ for efficient LP production**
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
レイアウト案生成システム
"""

from typing import Dict, Any, List
from datetime import datetime

class LayoutGenerator:
    def __init__(self):
        """初期化"""
        # レイアウトパターンライブラリ
        self.layout_patterns = {
            'hero': {
                'name': 'ヒーローレイアウト',
                'description': '商品画像を大きく、キャッチコピーとともに配置',
                'components': ['大型商品画像', 'メインキャッチ', 'サブキャッチ', '主要機能3点'],
                'composition': 'センター寄せ、縦配置',
                'image_ratio': '16:9または4:3',
                'text_area': '画像下部または右側30%'
            },
            'feature_grid': {
                'name': '機能グリッドレイアウト',
                'description': '複数機能を均等に配置',
                'components': ['機能アイコン×3-4', '機能名', '説明テキスト'],
                'composition': '3列または2×2グリッド',
                'image_ratio': '1:1（アイコン）',
                'text_area': '各グリッド下部25%'
            },
            'comparison': {
                'name': '比較レイアウト',
                'description': 'ビフォーアフターや競合比較',
                'components': ['比較画像×2', '矢印', '比較ポイント'],
                'composition': '左右分割',
                'image_ratio': '1:1（同サイズ）',
                'text_area': '中央および下部'
            },
            'lifestyle': {
                'name': 'ライフスタイルレイアウト',
                'description': '使用シーンを中心とした構成',
                'components': ['シーン画像', '人物', '商品', 'ライフスタイル提案'],
                'composition': '画像メイン、テキストオーバーレイ',
                'image_ratio': '16:9（横長）',
                'text_area': '画像内オーバーレイ'
            },
            'spec_table': {
                'name': 'スペック表レイアウト',
                'description': '仕様情報を整理して表示',
                'components': ['商品画像', 'スペック表', '寸法図', '認証マーク'],
                'composition': '左右分割（画像:表=1:1）',
                'image_ratio': '4:3',
                'text_area': '右側50%'
            },
            'testimonial': {
                'name': '証言・レビューレイアウト',
                'description': 'ユーザーの声や実績を表示',
                'components': ['ユーザー画像', '吹き出し', '星評価', '実績数値'],
                'composition': '吹き出し中心',
                'image_ratio': '1:1（ユーザー画像）',
                'text_area': '吹き出し内'
            }
        }
        
        # 業界別レイアウト推奨パターン
        self.industry_layouts = {
            'electronics': ['hero', 'feature_grid', 'spec_table', 'comparison'],
            'outdoor': ['lifestyle', 'hero', 'feature_grid', 'testimonial'],
            'lifestyle': ['lifestyle', 'hero', 'testimonial', 'feature_grid'],
            'fashion': ['lifestyle', 'hero', 'comparison', 'testimonial'],
            'home': ['lifestyle', 'feature_grid', 'spec_table', 'hero']
        }
    
    def generate_layout_suggestions(self, page_data: Dict, category: str = 'lifestyle') -> Dict:
        """ページ内容に基づいたレイアウト提案生成"""
        
        page_type = self._analyze_page_type(page_data)
        recommended_layouts = self._get_recommended_layouts(page_type, category)
        
        layout_suggestions = {
            'page_analysis': {
                'page_type': page_type,
                'category': category,
                'content_priority': page_data.get('design_priority', 'medium')
            },
            'recommended_layouts': [],
            'detailed_instructions': []
        }
        
        # 推奨レイアウトごとの詳細生成
        for i, layout_key in enumerate(recommended_layouts[:3]):  # 上位3つ
            layout_info = self.layout_patterns[layout_key]
            detailed_instruction = self._generate_detailed_instruction(
                layout_info, page_data, i == 0  # 最初のものを primary とする
            )
            
            layout_suggestions['recommended_layouts'].append({
                'layout_name': layout_info['name'],
                'layout_key': layout_key,
                'priority': 'primary' if i == 0 else 'alternative',
                'description': layout_info['description']
            })
            
            layout_suggestions['detailed_instructions'].append(detailed_instruction)
        
        return layout_suggestions
    
    def _analyze_page_type(self, page_data: Dict) -> str:
        """ページタイプを分析"""
        text = page_data.get('text', '').lower()
        layout_note = page_data.get('layout_note', '').lower()
        
        if any(word in text + layout_note for word in ['キャッチ', 'メイン', 'top', '商品名']):
            return 'hero'
        elif any(word in text + layout_note for word in ['機能', '特徴', 'feature']):
            return 'feature'
        elif any(word in text + layout_note for word in ['比較', 'vs', 'ビフォー', 'アフター']):
            return 'comparison'
        elif any(word in text + layout_note for word in ['シーン', 'ライフスタイル', '使用']):
            return 'lifestyle'
        elif any(word in text + layout_note for word in ['スペック', '仕様', 'サイズ']):
            return 'spec'
        elif any(word in text + layout_note for word in ['レビュー', '口コミ', '実績']):
            return 'testimonial'
        else:
            return 'general'
    
    def _get_recommended_layouts(self, page_type: str, category: str) -> List[str]:
        """ページタイプとカテゴリに基づく推奨レイアウト"""
        
        # ページタイプ別の基本推奨
        type_layouts = {
            'hero': ['hero', 'lifestyle'],
            'feature': ['feature_grid', 'hero'],
            'comparison': ['comparison', 'feature_grid'],
            'lifestyle': ['lifestyle', 'hero'],
            'spec': ['spec_table', 'feature_grid'],
            'testimonial': ['testimonial', 'hero']
        }
        
        base_layouts = type_layouts.get(page_type, ['hero', 'feature_grid'])
        category_layouts = self.industry_layouts.get(category, ['hero', 'lifestyle'])
        
        # 重複を避けつつマージ
        merged_layouts = []
        for layout in base_layouts + category_layouts:
            if layout not in merged_layouts:
                merged_layouts.append(layout)
        
        return merged_layouts[:4]  # 最大4つまで
    
    def _generate_detailed_instruction(self, layout_info: Dict, page_data: Dict, is_primary: bool) -> Dict:
        """詳細な制作指示を生成"""
        
        text_content = page_data.get('text', '')
        image_instruction = page_data.get('image_instruction', '')
        priority = page_data.get('design_priority', 'medium')
        
        instruction = {
            'layout_name': layout_info['name'],
            'priority': 'primary' if is_primary else 'alternative',
            'canvas_setup': {
                'size': 'PC: 1200×800px、SP: 850×1200px',
                'margin': 'PC: 60px、SP: 30px',
                'grid': self._generate_grid_system(layout_info)
            },
            'composition': {
                'main_area': self._generate_main_area_instruction(layout_info, text_content),
                'image_area': self._generate_image_area_instruction(layout_info, image_instruction),
                'text_area': self._generate_text_area_instruction(layout_info, text_content)
            },
            'visual_elements': {
                'typography': self._generate_typography_instruction(priority),
                'color_scheme': self._generate_color_instruction(priority),
                'spacing': self._generate_spacing_instruction(layout_info)
            },
            'responsive_notes': self._generate_responsive_instruction(layout_info)
        }
        
        return instruction
    
    def _generate_grid_system(self, layout_info: Dict) -> str:
        """グリッドシステムの指示生成"""
        layout_name = layout_info['name']
        
        if 'グリッド' in layout_name:
            return '3列グリッド（PC）、2列グリッド（SP）'
        elif '比較' in layout_name:
            return '2列グリッド（左右50%ずつ）'
        elif 'ヒーロー' in layout_name:
            return 'センタリング（最大幅1000px）'
        else:
            return '12列グリッドシステム'
    
    def _generate_main_area_instruction(self, layout_info: Dict, text_content: str) -> str:
        """メインエリアの構成指示"""
        composition = layout_info.get('composition', '')
        
        if 'センター' in composition:
            return f'中央寄せで配置、メインコンテンツを70%幅で配置'
        elif 'グリッド' in composition:
            return f'等間隔グリッド、各アイテム間に20pxの余白'
        elif '左右分割' in composition:
            return f'左右50%ずつ、中央に10pxのガター'
        else:
            return f'標準的な縦配置、適切な余白を確保'
    
    def _generate_image_area_instruction(self, layout_info: Dict, image_instruction: str) -> str:
        """画像エリアの指示"""
        ratio = layout_info.get('image_ratio', '16:9')
        
        base_instruction = f'アスペクト比: {ratio}、高品質画像を使用'
        if image_instruction and image_instruction != '【画像準備中】':
            return f'{base_instruction}\\n{image_instruction}'
        else:
            return base_instruction
    
    def _generate_text_area_instruction(self, layout_info: Dict, text_content: str) -> str:
        """テキストエリアの指示"""
        text_area = layout_info.get('text_area', '')
        
        instruction = f'配置: {text_area}'
        
        # テキスト量に応じた調整
        text_lines = len(text_content.split('\\n'))
        if text_lines > 5:
            instruction += '、長いテキストのため行間を調整'
        
        return instruction
    
    def _generate_typography_instruction(self, priority: str) -> str:
        """タイポグラフィの指示"""
        if priority == 'high':
            return 'メインタイトル: 32-40px、サブタイトル: 20-24px、本文: 16px（PC版）'
        elif priority == 'medium':
            return 'メインタイトル: 28-32px、サブタイトル: 18-20px、本文: 14px（PC版）'
        else:
            return 'メインタイトル: 24-28px、サブタイトル: 16-18px、本文: 14px（PC版）'
    
    def _generate_color_instruction(self, priority: str) -> str:
        """カラー指示"""
        if priority == 'high':
            return 'ブランドカラーをメインに、アクセントカラーで強調'
        else:
            return 'ブランドカラーを基調に、落ち着いた配色'
    
    def _generate_spacing_instruction(self, layout_info: Dict) -> str:
        """スペーシングの指示"""
        return 'セクション間: 60px、要素間: 20-30px、テキスト行間: 1.6-1.8'
    
    def _generate_responsive_instruction(self, layout_info: Dict) -> str:
        """レスポンシブ対応の指示"""
        return 'SP版では縦配置に変更、画像サイズとテキストサイズを最適化、タップ可能要素は44px以上'
    
    def generate_layout_document(self, all_pages_data: List[Dict], category: str = 'lifestyle') -> str:
        """全ページのレイアウト指示書を生成"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        document = f"""# LPレイアウト指示書
生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
カテゴリ: {category}

## 📋 全体構成
- 総ページ数: {len(all_pages_data)}枚
- カテゴリ最適化: {category}向けレイアウト
- レスポンシブ対応: PC/SP/タブレット

## 🎨 共通デザインシステム
### カラーパレット
- プライマリ: ブランドメインカラー
- セカンダリ: ブランドサブカラー  
- アクセント: 強調用カラー
- ニュートラル: #333（テキスト）、#F8F9FA（背景）

### タイポグラフィ
- 日本語フォント: Noto Sans JP推奨
- 英数字フォント: システムフォントまたはブランドフォント
- 行間: 1.6-1.8（読みやすさ重視）

### スペーシングシステム
- 基本単位: 8px
- セクション間: 64px（8×8）
- 要素間: 24px（8×3）
- 内部余白: 16px（8×2）

---

"""
        
        # 各ページの詳細レイアウト指示
        for i, page_data in enumerate(all_pages_data, 1):
            layout_suggestions = self.generate_layout_suggestions(page_data, category)
            
            document += f"""## 📄 {i}枚目レイアウト指示

### ページ分析
- タイプ: {layout_suggestions['page_analysis']['page_type']}
- 優先度: {layout_suggestions['page_analysis']['content_priority']}

### 推奨レイアウト（第1案）
**{layout_suggestions['recommended_layouts'][0]['layout_name']}**

#### 🖼️ 構成要素
{layout_suggestions['detailed_instructions'][0]['composition']['main_area']}

#### 📸 画像指示
{layout_suggestions['detailed_instructions'][0]['composition']['image_area']}

#### ✏️ テキスト配置
{layout_suggestions['detailed_instructions'][0]['composition']['text_area']}

#### 🎨 ビジュアル仕様
- {layout_suggestions['detailed_instructions'][0]['visual_elements']['typography']}
- {layout_suggestions['detailed_instructions'][0]['visual_elements']['color_scheme']}
- {layout_suggestions['detailed_instructions'][0]['visual_elements']['spacing']}

#### 📱 レスポンシブ対応
{layout_suggestions['detailed_instructions'][0]['responsive_notes']}

### 代替案
"""
            # 代替案も追加
            for j, alt_layout in enumerate(layout_suggestions['recommended_layouts'][1:], 1):
                document += f"**案{j+1}**: {alt_layout['layout_name']} - {alt_layout['description']}\\n"
            
            document += "\\n---\\n\\n"
        
        # 制作ワークフロー
        document += """## 🔄 制作ワークフロー

### Phase 1: デザインカンプ作成
1. ワイヤーフレーム確認
2. ビジュアルデザイン作成
3. レビュー・修正

### Phase 2: レスポンシブ対応
1. SP版デザイン作成
2. タブレット版調整
3. 動作確認

### Phase 3: 最終調整
1. 全体統一感チェック
2. アクセシビリティ確認
3. 納品準備

## ✅ チェックリスト
- [ ] ブランドガイドライン準拠
- [ ] 読みやすいフォントサイズ
- [ ] 十分なコントラスト比
- [ ] タップ可能要素のサイズ（44px以上）
- [ ] 画像の最適化
- [ ] ローディング速度
"""
        
        return document
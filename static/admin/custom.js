// Django Admin 自定义JavaScript - 中文化和功能增强

document.addEventListener('DOMContentLoaded', function() {
    console.log('Django Admin 自定义脚本加载中...');
    
    // 中文化函数
    function translatePage() {
        // 替换帮助文本
        const helpTexts = document.querySelectorAll('.help, .help-block, small, .help-text');
        helpTexts.forEach(function(element) {
            let text = element.textContent;
            
            // 标签选择器帮助文本
            if (text.includes('Choose') && text.includes('标签')) {
                element.textContent = '在左侧选择标签后点击右箭头添加；在右侧选择后点击左箭头移除';
            } else if (text.includes('Remove') && text.includes('标签')) {
                element.textContent = '在右侧选择标签后点击左箭头移回左侧';
            }
            
            // 通用替换
            text = text.replace(/Choose/g, '选择');
            text = text.replace(/Select/g, '选择');
            text = text.replace(/Remove/g, '移除');
            text = text.replace(/Available/g, '可用');
            text = text.replace(/Chosen/g, '已选择');
            text = text.replace(/Filter/g, '筛选');
            text = text.replace(/Search/g, '搜索');
            
            element.textContent = text;
        });
        
        // 替换按钮文本
        const buttons = document.querySelectorAll('input[type="submit"], button, .button, .btn');
        buttons.forEach(function(button) {
            let text = button.value || button.textContent;
            
            if (text.includes('Save')) {
                if (button.value) button.value = '保存';
                else button.textContent = '保存';
            } else if (text.includes('Add another')) {
                button.textContent = '添加另一个';
            } else if (text.includes('Delete')) {
                button.textContent = '删除';
            } else if (text.includes('Add')) {
                button.textContent = '添加';
            } else if (text.includes('Change')) {
                button.textContent = '修改';
            }
        });
        
        // 替换链接文本
        const links = document.querySelectorAll('a');
        links.forEach(function(link) {
            let text = link.textContent.trim();
            
            if (text === 'Add') {
                link.textContent = '添加';
            } else if (text === 'Change') {
                link.textContent = '修改';
            } else if (text === 'Delete') {
                link.textContent = '删除';
            } else if (text.includes('Add another')) {
                link.textContent = '添加另一个';
            }
        });
        
        // 替换表格标题
        const tableHeaders = document.querySelectorAll('th');
        tableHeaders.forEach(function(th) {
            let text = th.textContent;
            if (text.includes('ACTIONS')) {
                th.textContent = '操作';
            }
        });
        
        // 替换面包屑导航
        const breadcrumbs = document.querySelectorAll('.breadcrumbs a, .breadcrumbs');
        breadcrumbs.forEach(function(crumb) {
            let text = crumb.textContent;
            text = text.replace(/App/g, '应用');
            text = text.replace(/Articles/g, '文章');
            text = text.replace(/article/g, '文章');
            text = text.replace(/Comments/g, '评论');
            text = text.replace(/Tags/g, '标签');
            text = text.replace(/Users/g, '用户');
            text = text.replace(/Groups/g, '组');
            crumb.textContent = text;
        });
    }
    
    // 增强Markdown编辑器
    function enhanceMarkdownEditor() {
        // 等待Markdownx编辑器加载
        setTimeout(function() {
            const markdownFields = document.querySelectorSelectorAll('.markdownx');
            markdownFields.forEach(function(field) {
                // 添加自定义样式
                field.style.background = 'rgba(30, 41, 59, 0.9)';
                field.style.color = '#e2e8f0';
                field.style.border = '1px solid rgba(56, 189, 248, 0.3)';
                field.style.borderRadius = '4px';
                field.style.padding = '12px';
                field.style.fontFamily = 'monospace';
                field.style.fontSize = '14px';
                field.style.lineHeight = '1.5';
                field.style.minHeight = '300px';
                
                // 添加占位符
                if (!field.placeholder) {
                    field.placeholder = '在这里输入Markdown内容...\n\n支持语法高亮、表格、列表等功能';
                }
            });
            
            // 查找Markdownx预览区域
            const previewAreas = document.querySelectorAll('.markdownx-preview');
            previewAreas.forEach(function(preview) {
                preview.style.background = 'rgba(15, 23, 42, 0.9)';
                preview.style.color = '#e2e8f0';
                preview.style.border = '1px solid rgba(56, 189, 248, 0.2)';
                preview.style.borderRadius = '4px';
                preview.style.padding = '15px';
                preview.style.marginTop = '10px';
                preview.style.minHeight = '300px';
            });
        }, 1000);
    }
    
    // 增强文件上传
    function enhanceFileUpload() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(function(input) {
            input.addEventListener('change', function(e) {
                const fileName = e.target.files[0]?.name || '未选择文件';
                const fileText = e.target.nextElementSibling;
                if (fileText && fileText.classList.contains('file-upload-text')) {
                    fileText.textContent = fileName;
                }
            });
        });
    }
    
    // 添加键盘快捷键
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl+S 保存
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                const saveButton = document.querySelector('input[type="submit"][name="_save"], input[type="submit"]:first-of-type');
                if (saveButton) {
                    saveButton.click();
                }
            }
            
            // Ctrl+Enter 快速保存并继续编辑
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                const continueButton = document.querySelector('input[type="submit"][name="_continue"], input[type="submit"][value*="保存并继续"]');
                if (continueButton) {
                    continueButton.click();
                }
            }
        });
    }
    
    // 添加工具提示
    function addTooltips() {
        const helpIcons = document.querySelectorAll('.help-icon, .icon-help, img[src*="help"], img[src*="unknown"]');
        helpIcons.forEach(function(icon) {
            icon.title = '点击查看帮助信息';
        });
        
        const addIcons = document.querySelectorAll('.addlink, .add-another, img[src*="icon-add"]');
        addIcons.forEach(function(icon) {
            icon.title = '添加新项目';
        });
        
        const changeIcons = document.querySelectorAll('.changelink, img[src*="icon-changelink"]');
        changeIcons.forEach(function(icon) {
            icon.title = '编辑此项目';
        });
        
        const deleteIcons = document.querySelectorAll('.deletelink, img[src*="icon-deletelink"]');
        deleteIcons.forEach(function(icon) {
            icon.title = '删除此项目';
        });
    }
    
    // 初始化所有功能
    function initialize() {
        translatePage();
        enhanceMarkdownEditor();
        enhanceFileUpload();
        addKeyboardShortcuts();
        addTooltips();
        
        console.log('Django Admin 自定义脚本加载完成');
    }
    
    // 页面加载完成后初始化
    initialize();
    
    // 监听DOM变化，处理动态加载的内容
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // 重新应用中文化
                setTimeout(translatePage, 100);
            }
        });
    });
    
    // 开始观察
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 页面卸载时停止观察
    window.addEventListener('beforeunload', function() {
        observer.disconnect();
    });
});
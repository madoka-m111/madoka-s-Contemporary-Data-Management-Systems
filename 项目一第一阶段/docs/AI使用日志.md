# AI 使用日志

> 说明：日志中的用户需求用于概括当次任务目标，部分内容为事后根据实际改动整理，非逐字对话记录。

## 2026-10-15，使用记录1，bash，创建项目目录结构，创建了 app、config、templates、tests、scripts、docs 等目录及其子目录，用户要求生成完整项目结构

## 2026-10-15，使用记录2，bash，创建所有模块的空占位文件，包括 models、routes、services、utils、static、templates、tests、scripts、docs 下的所有 .py、.js、.css、.html、.md 文件，用户要求只完成目录创建不编写内容

## 2026-10-15，使用记录3，write，config/settings.py，编写配置类包含开发/生产/测试环境配置、MongoDB连接、JWT、CORS等，用户要求完善配置文件

## 2026-10-15，使用记录4，write，app/__init__.py，编写Flask应用工厂函数、MongoDB连接、蓝图注册、索引初始化，用户要求初始化Flask应用

## 2026-10-15，使用记录5，write，app/models/user.py、survey.py、question.py、response.py，编写四个MongoDB数据模型类包含CRUD方法和索引，用户要求创建数据模型层

## 2026-10-15，使用记录6，write，docs/数据库设计.md，编写MongoDB Schema设计文档包含四个集合定义、索引、关系图、常用查询，用户要求设计MongoDB schema

## 2026-10-15，使用记录7，write，docs/数据库设计.md，将文档中的所有英文注释翻译为中文，用户要求注释改为中文

## 2026-10-15，使用记录8，write，docs/API说明.md，编写完整API接口文档包含认证、用户、问卷、题目、填写、统计等6大模块共30+个接口，用户要求完成API设计

## 2026-10-15，使用记录9，write，app/services/validation_service.py，实现答案校验服务支持9种题型的校验逻辑（长度、范围、正则、选项等），用户要求实现校验逻辑

## 2026-10-15，使用记录10，write，app/services/jump_service.py，实现跳转逻辑服务支持条件判断（equals/not_equals/contains/greater_than/less_than）、显示/隐藏/跳转动作、下一题计算，用户要求实现跳转逻辑

## 2026-10-15，使用记录11，write，app/services/survey_service.py、question_service.py、response_service.py、stats_service.py、user_service.py，实现核心业务服务层，用户要求完成核心功能实现

## 2026-10-15，使用记录12，write，app/routes/auth_routes.py、survey_routes.py、fill_routes.py、stats_routes.py，实现API路由层包含认证、问卷管理、题目管理、填写提交、统计导出等完整接口，用户要求完成核心功能实现

## 2026-10-15，使用记录13，write，app/utils/validators.py、response_util.py，实现通用校验函数和统一响应格式工具，用户要求完成核心功能实现

## 2026-10-16，使用记录14，write，frontend/login.html，frontend/register.html，实现登录和注册页面，包含JWT认证、表单校验、错误提示，用户要求编写前端代码

## 2026-10-16，使用记录15，write，frontend/dashboard.html，实现问卷管理页面，包含问卷列表、状态筛选、发布/删除操作，用户要求编写前端代码

## 2026-10-16，使用记录16，write，frontend/create.html，frontend/edit.html，实现创建和编辑问卷页面，包含题目增删改排序、选项编辑、问卷设置，用户要求编写前端代码

## 2026-10-16，使用记录17，write，frontend/survey.html，实现填写问卷页面，支持9种题型、跳转逻辑、必填校验、草稿自动保存、匿名填写，用户要求编写前端代码

## 2026-10-16，使用记录18，write，frontend/stats.html，实现统计结果页面，包含总览指标、每日趋势图、各题型统计图表、多格式导出，用户要求编写前端代码

## 2026-10-16，使用记录19，write，frontend/create.html，增强创建问卷页面，添加跳转逻辑配置UI（源题目/条件/比对值/目标题目/动作），支持题目动态增删排序、选项编辑，用户要求实现创建问卷页跳转配置功能

## 2026-10-16，使用记录20，write，frontend/survey.html，增强填写问卷页面，完善跳转逻辑处理（条件判断、动态显隐题目）、实时必填校验、答题进度、已作答标记、匿名填写支持，用户要求实现填写问卷页跳转处理和实时校验功能

## 2026-10-16，使用记录21，write，frontend/stats.html，增强统计页面，集成Chart.js图表库，替换CSS条形图为柱状图/环形图/折线图，支持单选/多选/下拉/数值/文本/日期等题型可视化，用户要求实现统计页Chart.js图表功能

## 2026-10-16，使用记录22，write，requirements.txt，补全Python依赖列表，包含Flask、flask-cors、flask-jwt-extended、pymongo、python-dotenv、pytest、mongomock、werkzeug，用户要求编写测试用例需要依赖

## 2026-10-16，使用记录23，write，tests/conftest.py，编写pytest配置文件，提供app/client/db/auth_headers/survey_id fixture，使用mongomock模拟MongoDB，用户要求编写测试用例

## 2026-10-16，使用记录24，write，tests/test_auth.py，编写用户注册登录测试用例，包含注册成功、重复注册、缺少字段、登录成功、密码错误、用户不存在、获取当前用户、无token访问等8个测试，用户要求编写测试用例

## 2026-10-16，使用记录25，write，tests/test_survey_create.py，编写问卷管理测试用例，包含创建问卷、缺少标题、获取我的问卷、无token访问、公开问卷列表、问卷详情、更新问卷、发布问卷、关闭问卷、删除问卷等10个测试，用户要求编写测试用例

## 2026-10-16，使用记录26，write，tests/test_question_add.py，编写题目管理测试用例，包含添加题目、缺少字段、已发布问卷添加题目、批量添加题目、获取题目列表、修改题目、删除题目、调整题目顺序等8个测试，用户要求编写测试用例

## 2026-10-16，使用记录27，write，tests/test_jump_logic.py，编写跳转逻辑单元测试用例，包含等于/不等于/包含/大于/小于条件判断、显示/隐藏动作、下一题计算等9个测试，用户要求编写测试用例

## 2026-10-16，使用记录28，write，tests/test_validation.py，编写答案校验单元测试用例，包含必填校验、单选/多选校验、文本长度校验、数字范围校验、评分范围校验、批量校验等7个测试，用户要求编写测试用例

## 2026-10-16，使用记录29，write，tests/test_submit.py，编写提交问卷测试用例，包含开始填写、未发布问卷填写、保存草稿、校验答案、提交问卷、缺少必填项提交等6个测试，用户要求编写测试用例

## 2026-10-16，使用记录30，write，tests/test_stats.py，编写统计测试用例，包含获取问卷统计、获取题目统计、导出回答数据、无token访问等4个测试，用户要求编写测试用例

## 2026-10-17，使用记录31，background_process，启动MongoDB实例，运行 D:\MongoDB\bin\mongod.exe --dbpath D:\mongodb-data --port 27017，数据库已就绪，用户要求启动mongodb实现数据库

## 2026-10-17，使用记录32，write，docs/数据库设计.md，补充设计说明章节：四个集合分离的职责边界、为什么不用关系数据库（题型多样/结构动态/跳转逻辑动态/读多写少）、为什么适合MongoDB（无固定Schema/嵌入式文档/数组原生支持/聚合框架/水平扩展）、三条设计建议的遵循情况（勿单集合/谨慎冗余/逻辑不写死），用户要求完善MongoDB设计要求说明

## 2026-10-17，使用记录33，edit，frontend/survey.html、frontend/dashboard.html，修复 JWT token 过期导致填写页显示“无法开始填写”及返回后问卷列表全面 401 加载失败的问题：survey.html 新增 tryStart 封装，遇到 401 时自动清除失效 token 并以匿名身份重试；dashboard.html 在 401 时清除本地存储并跳转登录页，用户要求修正问卷填写页与主页鉴权失效导致的功能不可用问题

## 2026-10-17，使用记录34，edit，app/services/survey_service.py、frontend/dashboard.html，修复提交问卷后用户主页回答数不增加且页面不刷新的问题：survey_service.py 的 list_user_surveys 中为每个问卷新增 response_count 统计（按 submitted 状态回答数查询）；dashboard.html 添加 pageshow 事件监听，页面重新显示时自动重新加载问卷列表，用户要求修正提交后回答数未更新与列表未刷新的问题

## 2026-10-18，使用记录35，edit，frontend/dashboard.html，为创建问卷者在主页添加查看问卷统计功能：在每个问卷操作列新增“统计”按钮（绿色），点击后跳转至 stats.html?id=<survey_id>，复用现有统计页面展示总回答数、完成率、平均耗时、每日趋势图及各题型详细统计图表，后端已有 /api/stats/surveys/<survey_id> 接口并做创建者权限校验，用户要求在主页直接进入问卷数据统计

## 2026-10-18，使用记录36，edit，frontend/stats.html，修复统计界面打开显示“网络错误”的问题：stats.html:100 的 fetch 响应未调用 await res.json() 直接使用 res.data（Response 对象无 data 属性），导致 stats 为 undefined，访问 stats.total_responses 抛出异常被 catch 显示“网络错误”；已改为 const data = await res.json(); const stats = data.data；用户要求修正统计页无法加载数据的问题

## 2026-10-18，使用记录37，edit，frontend/stats.html，删除页面中重复的每日提交趋势图表：原静态 HTML 中的 chart-card（canvas id=trendChart）与 renderTrendChart() 动态生成的 chart-card（canvas id=trendCanvas）重复导致页面显示两个趋势图，已删除静态重复项，仅保留动态生成的一个，用户要求删除多余趋势图

## 2026-10-18，使用记录38，edit，app/services/stats_service.py、frontend/stats.html，修复平均耗时逻辑问题：stats_service.py 原用 MongoDB 聚合 $avg 嵌套 $subtract 日期字段计算平均耗时，在部分环境下兼容性差且 int() 向下取整丢失精度，已改为在 Python 端查询所有 submitted 响应并按 (submitted_at - started_at).total_seconds() 计算平均，保留一位小数；frontend/stats.html 新增 formatDuration() 将秒数格式化为“X分Y秒”并显示，用户要求修正平均耗时显示异常的问题

## 2026-10-18，使用记录39，edit，app/services/stats_service.py，平均耗时仍显示 0 秒的进一步修复：移除了 db.responses.find 中冗余的 'started_at': {'$exists': True} 和 'submitted_at': {'$exists': True} 过滤条件（这些条件可能把字段存在但为 None 的文档排除，导致 durations 为空返回 0），改为仅按 survey_id 和 status 查询，在 Python 端通过 if started and submitted 和 try/except 做空值与类型容错，用户要求彻底修正平均耗时为 0 的问题

## 2026-10-18，使用记录40，edit，frontend/stats.html，删除平均耗时板块：移除了 stats-grid 中的“平均耗时” stat-card、删除前端设置 statAvg 的代码、删除 formatDuration() 辅助函数，页面统计概览仅保留“总回答数”与“完成率”两项，用户要求删掉平均耗时这一板块

## 2026-10-18，使用记录41，edit，frontend/create.html、frontend/edit.html，添加问卷截止日期设定功能：create.html 和 edit.html 在问卷描述字段后新增“截止日期” datetime-local 输入框，支持设置问卷填写截止时间；create.html 创建时将 deadline 字段随请求发送至后端；edit.html 加载时将 ISO 格式的 deadline 转换为 datetime-local 格式回填，保存时随 PUT 请求一并提交，已发布问卷时禁用该输入框，用户要求在创建问卷时支持设定截止日期

## 2026-10-18，使用记录42，edit，app/services/survey_service.py、frontend/create.html、frontend/edit.html，添加截止日期必须在当前时间之后的验证：后端 create_survey 和 update_survey 中新增验证，若 deadline 不为空且 <= 当前时间则拒绝并返回错误；前端 create.html 和 edit.html 在表单提交前做客户端校验，选中的截止日期若不晚于当前时间则阻止提交并提示“截止日期必须在当前时间之后”，用户要求截止日期不能填过去的日期

## 2026-10-18，使用记录43，edit，frontend/dashboard.html，删除状态筛选中的“已关闭”芯片：sidebar 状态筛选只保留“全部”“草稿”“已发布”三个芯片，移除了 data-status="closed" 的“已关闭”芯片，用户要求首页“已关闭”筛选栏没什么用，删掉它

## 2026-10-18，使用记录44，edit，app/services/survey_service.py、app/routes/survey_routes.py、frontend/dashboard.html，添加已发布问卷撤回功能：后端新增 unpublish_survey 服务方法和 /api/surveys/<id>/unpublish 路由，仅允许创建者将已发布问卷撤回为草稿状态；前端 dashboard.html 在已发布问卷操作列新增橙色“撤回”按钮，点击后确认并调用接口，成功后重新加载列表，用户要求添加撤回功能以便继续编辑问卷

## 2026-10-18，使用记录45，edit，frontend/edit.html，删除编辑问卷页内部的链接显示：移除了 status-row 中的 link-box（输入框+复制按钮）、删除了 loadSurvey 中的 linkBox/linkInput 回填代码、删除了 copyLink 函数，问卷链接仅保留首页 dashboard 点击“填写链接”生成，用户要求编辑问卷内部不需要显示链接

## 2026-10-18，使用记录46，edit，frontend/edit.html，编辑问卷页面中“必填题”三字居中：给必填题复选框标签添加 justify-content:center，使复选框与“必填题”文字整体居中对齐，用户要求将“必填题”三字居中放置

## 2026-10-18，使用记录47，edit，frontend/edit.html，必填题居中进一步修复：前一次 justify-content:center 未生效，因 label 默认宽度未撑满；已改为外层 div 设 text-align:center、label 改为 display:inline-flex，使整个“[复选框] 必填题”组合在父容器中水平居中，用户要求必填题三字居中

## 2026-10-18，使用记录48，edit，frontend/edit.html，必填题强制居中最终修复：将必填题所在父 div 改为 display:flex; justify-content:center，强制整个“[复选框] 必填题”组合在父容器中水平居中，确保“必填题”三字不再偏右，用户反馈仍未居中后采用最强制的 flex 居中方案，用户要求“必填题”三字必须严格水平居中

## 2026-10-18，使用记录49，edit，frontend/create.html，创建问卷页面“必填题”居中：将 create.html 中必填题所在父 div 改为 display:flex; justify-content:center，label 改为 inline-flex，使整个“[复选框] 必填题”组合水平居中，与 edit.html 保持一致，用户反馈创建页必填题仍未居中，用户要求创建页与编辑页保持一致并完成居中修复

## 2026-10-18，使用记录50，edit，frontend/create.html、frontend/edit.html，问卷题型仅保留单选题、多选题和填空题：create.html 和 edit.html 中 questionTypes 数组精简为 single_choice（单选题）、multiple_choice（多选题）、text（填空题）三种；edit.html 的 typeLabel 映射同步精简；用户要求题型仅保留这三种

## 2026-10-18，使用记录51，edit，frontend/survey.html，修复填空题输入一个字符后无法继续输入的问题：saveAns 每次输入都会调用 renderQuestion，而 renderQuestion 通过 innerHTML 重建整个 DOM 导致输入框失去焦点；在 renderQuestion 末尾添加焦点恢复逻辑，重新聚焦到当前题目的输入元素，并将光标移到末尾，用户要求修正填空题无法连续输入的问题

## 2026-10-18，使用记录52，edit，frontend/survey.html，修复问卷链接打开页面空白的问题：renderQuestion 函数中 const q 重复声明（第150行和第212行），导致 JavaScript 语法错误，页面无法渲染任何内容；已删除第212行重复声明，直接复用第150行已定义的 q 变量，用户反馈问卷链接打开啥也没有，用户要求修复填写页空白问题

## 2026-10-18，使用记录53，edit，frontend/survey.html，修复填写时无法输入中文的问题：saveAns 绑定在 oninput 上，每次按键都会触发 renderQuestion 通过 innerHTML 重建 DOM，打断中文输入法的 composition 过程，导致只能输入英文字符；新增 isComposing 标志，textarea 增加 oncompositionstart/oncompositionend 事件，组词期间不触发 saveAns，组词结束后再保存一次，用户要求修正无法输入中文的问题

## 2026-10-18，使用记录54，edit，frontend/survey.html，彻底修复无法输入中文问题：isComposing 方案不足，用户输入英文字符时 isComposing 为 false，每次按键仍调用 renderQuestion 重建 DOM 导致输入法无法工作；最终方案：saveAns、saveMulti、saveFile 不再调用 renderQuestion，只更新答案状态；DOM 重建仅在 nextQ/prevQ 切换题目时进行，输入时不再打断 IME，用户反馈仍无法输入中文，用户要求彻底解决中文输入法无法输入的问题

## 2026-10-18，使用记录55，edit，frontend/create.html、frontend/edit.html，将填空题分为文本填空题和数字填空题：create.html 和 edit.html 的 questionTypes 中 text 改为“文本填空题”，新增 number“数字填空题”；typeLabel 映射同步精简为 single_choice/多选题/text/文本填空题/number/数字填空题；survey.html 已有 number 分支（<input type="number">）且 saveAns 不再重建 DOM，数字填空可正常输入；validation_service.py number 类型走 _validate_number，非数字输入会报错；stats_service.py number 类型走 _stats_numeric，统计结果中已包含 avg（平均值）；用户要求把填空题细分为文本填空题和数字填空题，方便分别设置校验规则和统计方式

## 2026-10-18，使用记录56，edit，frontend/create.html，改造跳转逻辑配置 UI 使其更清晰：将原来横向拥挤的四个下拉框+输入框改为垂直表单布局，每个字段带清晰标签（当/的条件/值/时，对/执行）；新增逻辑预览文本（如"当第1题等于"A"时，跳转到第3题"），使条件→动作的流向一目了然；保留清除按钮和示例提示，后端 jump_logic 字段结构不变，用户反馈跳转逻辑不够清晰、不好选择，用户要求重新设计更直观的跳转逻辑配置界面

## 2026-10-18，使用记录57，edit，frontend/edit.html，修复草稿编辑时跳转逻辑丢失问题：edit.html 的 renderQuestions 原本没有跳转逻辑配置 UI，用户打开草稿编辑时既看不到跳转逻辑也无法修改，误认为数据丢失；已为每个题目添加与 create.html 一致的跳转逻辑配置卡片（垂直表单布局，包含源题目/条件/值/目标题目/动作），新增 toggleJump、clearJump、updateJump 函数；已发布问卷时跳转逻辑 UI 隐藏，仅草稿状态可编辑；save 时已随 body 发送 jump_logic，数据未真正丢失，现通过 UI 展示修正，用户反馈草稿中打开跳转逻辑会丢失，用户要求在编辑页补齐跳转逻辑配置

## 2026-10-18，使用记录58，edit，frontend/edit.html，修复草稿保存修改点了没反应问题：保存逻辑中未检查 fetch 响应的 res.ok，后端返回 400/500 时前端不显示错误；未检查 surveyId 是否存在；若 loadSurvey 失败导致 survey 为 null，survey.status !== 'draft' 会为 true，错误地禁用 btnSave；已添加 surveyId 存在性检查，在每个 fetch 后检查 res.ok 并显示后端返回的错误消息，用户反馈草稿保存点击后无任何反应，用户要求修复保存无反馈问题

## 2026-10-18，使用记录59，edit，frontend/edit.html，修复保存修改时题目更新返回 405 问题：后端 `survey_bp` 蓝图注册前缀为 `/api/surveys`，题目更新路由完整路径为 `/api/surveys/questions/<question_id>`，但前端 edit.html 中调用的是 `/api/questions/<question_id>`，路径不匹配导致 405 Method Not Allowed；已将前端题目 PUT 请求 URL 改为 `${API}/surveys/questions/${qid}`，与后端蓝图前缀一致，用户反馈草稿保存修改有题目接口返回 405，用户要求修复题目更新接口路径

## 2026-10-18，使用记录60，edit，frontend/edit.html，修复保存修改按钮点击无反应问题：btnSave 按钮位于顶部导航栏 `.nav` 内，不在 `surveyForm` 表单内，点击按钮不会触发表单的 submit 事件，导致保存逻辑根本不执行；已将保存逻辑从表单 submit 事件改为直接绑定到 btnSave 的 click 事件，并保留 showMsg('保存成功', 'success') 的成功反馈，用户反馈点击保存修改没有任何反应，用户要求修复保存按钮无响应问题

## 2026-10-18，使用记录61，edit，frontend/create.html、frontend/edit.html，修改跳转逻辑值字段为根据源题目选项联动：create.html 和 edit.html 的跳转逻辑配置中，"值"字段不再是手动输入文本，而是根据选中的源题目类型动态生成；源题目为单选题时显示选项下拉框，源题目为多选题时显示多选下拉框，源题目为文本/数字等其他类型时保留文本输入；新增 onJumpSrcChange 函数，选择源题目后自动清空值并重新渲染；updateJump 支持读取 select multiple 的多个选中值，用户反馈跳转逻辑中比对值应根据源题目配置的选项来选择，用户要求将比对值改为与源题目选项联动

## 2026-10-18，使用记录62，edit，frontend/login.html、frontend/register.html、frontend/dashboard.html、frontend/create.html、frontend/edit.html、frontend/survey.html、frontend/stats.html、app/__init__.py、README.md，修复登录和注册页面提示“网络错误”：原前端用 location.origin 拼接 API 地址，若通过 VS Code Live Server（5500 等端口）或非 Flask 静态服务器打开页面，请求会被发到静态服务器并返回 404 HTML，res.json() 解析失败后被 catch 统一显示为“网络错误”；现改为仅当页面在 5000 端口时使用同源 /api，否则自动请求 `http://<当前主机>:5000/api`，并支持 window.API_BASE 或 localStorage.survey_api_base 覆盖；登录/注册先读取响应文本再解析 JSON，非 JSON 响应会显示 HTTP 状态和实际请求地址，fetch 的 TypeError 会提示检查 python run.py 与 MongoDB；后端新增 /frontend/<path> 路由兼容旧地址；README 增加“网络错误”排查步骤；用户要求排查并修复登录、注册等页面在 Live Server 下提示“网络错误”的问题，并补充相应的排查说明

## 2026-10-18，使用记录63，edit，frontend/create.html、frontend/edit.html、app/models/survey.py、tests/test_survey_create.py，修复点击“跳转逻辑”后问卷页空白并提示网络错误的问题：题目卡片内多个动态生成的按钮未声明 type，默认 type="submit"，点击“显示/隐藏跳转逻辑”“清除跳转逻辑”“上移/下移/删除题目”“添加/删除选项”会触发表单提交；create.html 因此意外创建问卷并跳转，edit.html 以 GET 提交表单导致地址栏丢失 ?id=，随后请求 /api/surveys/null 返回 500。已为所有动态按钮添加 type="button"，edit.html 增加表单 submit 防刷新处理并校验 surveyId 必须为 24 位 ObjectId，ID 缺失时直接提示且不发请求；app/models/survey.py 的 find_by_id 增加 ObjectId 合法性校验，非法 ID 统一返回 404；新增非法 ID 回归测试，pytest 67 passed；用户要求修复点击“跳转逻辑”后页面空白、地址栏丢失 id 并提示网络错误的问题

## 2026-10-18，使用记录64，edit，frontend/create.html、frontend/edit.html，修复选择跳转逻辑源题目后配置卡片自动收起的问题：跳转卡片的展开状态原先只由 `jump_logic.condition` 决定，选择“当”后面的源题目会触发 `onJumpSrcChange` → `renderQuestions()`，此时条件尚未选择，重新渲染后卡片便失去 `show` 类并被收起；同时 `updateJump()` 在任一字段未填全时会将整个 `jump_logic` 置空，导致半填写的条件丢失。现改为用题目上的 `_jumpOpen` 独立记录展开状态（已有跳转逻辑时默认展开），选择源题目/执行动作时显式保持展开，展开按钮文案同步更新；`updateJump()` 改为保留已填写的部分配置，仅在源题目为空时清空，完整性和比对值仍由保存前校验拦截；create.html 保存时剔除 `_tmpId`、`_jumpOpen` 临时字段；用户要求修复选择跳转逻辑源题目后卡片自动收起、已填条件丢失的问题

## 2026-10-18，使用记录65，edit，frontend/create.html、frontend/edit.html，为跳转逻辑增加独立保存按钮：原先跳转条件修改后直接写入内存中的 `jump_logic`，没有单独保存入口和反馈，用户无法确认本次调整是否生效。现为每个跳转逻辑卡片增加“保存跳转逻辑”按钮，字段变化先写入 `_jumpDraft` 草稿并显示“有未保存的修改”，点击保存后统一校验源题目、条件、比对值、目标题目与动作，再写入 `jump_logic` 并显示“保存成功”；edit.html 对已有题目立即调用 `PUT /api/surveys/questions/<id>` 持久化跳转逻辑，创建页和尚未保存的新题目则提示“保存问卷后生效”；保存前校验会拦截未保存草稿，避免整份问卷保存时绕过独立保存；edit.html 清除跳转逻辑时同步清空服务器数据，create.html 保存时剔除 `_jumpDraft` 临时字段。Node 函数级仿真通过，pytest 67 passed；用户要求给跳转逻辑增加独立保存按钮，修改后点击保存才生效，并给出“保存成功”的反馈

## 2026-10-18，使用记录66，edit，frontend/create.html、frontend/edit.html、frontend/survey.html、tests/test_validation.py、README.md、docs/测试用例.md，为文本填空题和数字填空题增加限制条件：文本填空题支持最少字数和最多字数，数字填空题支持最小值、最大值和“仅允许整数”，同时保留多选题原有的最少/最多选择数；创建页和编辑页将原有限制输入改为与跳转逻辑一致的折叠卡片，新增“显示/隐藏限制条件”、限制摘要、独立“保存限制条件”和“清除限制条件”按钮；字段变化先写入 `_validationDraft` 草稿并显示“有未保存的修改”，点击保存后才写入 `validation`，编辑页对已有题目通过 `PUT /api/surveys/questions/<id>` 立即持久化，创建页和未保存的新题目提示“保存问卷后生效”，已发布问卷禁用编辑；整卷保存前会校验限制规则并拦截未保存的限制草稿，创建页提交题目时剔除 `_validationDraft`、`_validationOpen` 临时字段；填写页根据配置为文本输入设置 `minlength/maxlength`、为数字输入设置 `min/max/step`，并显示限制提示，在“下一题/提交”前执行同样的长度、范围与整数前端校验，后端 `ValidationService` 继续兜底；补充 `integer_only` 单元测试，pytest 68 passed，三个页面内联 JavaScript 通过 `node --check`，函数级行为仿真通过；用户要求文本填空限制最少/最多输入字数，数字填空限制最小值、最大值和是否必须为整数，并将限制窗口设置为类似跳转逻辑的样式



## 2026-10-18，使用记录67，edit，app/services/validation_service.py、frontend/create.html、frontend/edit.html、frontend/survey.html、tests/test_validation.py、README.md、docs/测试用例.md、docs/关键逻辑说明.md、docs/项目完成报告.md，为多选题增加精确选择数量限制：在原有 min_select/max_select 基础上新增 exact_select（必须选择数），创建页和编辑页限制卡片新增“必须选择数”输入，限制摘要、保存校验与清除逻辑同步支持；exact_select 与最少/最多选择数互斥，且不能超过选项总数，最少选择数也补充了选项总数上限校验；填写页显示“必须选择 X 个选项/至少选择/最多选择”提示，下一题与提交前校验选择数量，后端 ValidationService 对空答和数量不符统一兜底，仅设置 max_select 时仍允许跳过；补充 3 个单元测试覆盖 min/max、exact 和空答语义，pytest 71 passed，三个页面内联 JavaScript 通过 node --check，函数级行为仿真通过；用户要求多选题支持至少选择 2 个、最多选择 3 个、必须选择 2 个等数量限制并在填写时检查


## 2026-10-18，使用记录68，edit，docs/项目完成报告.md、docs/关键逻辑说明.md、README.md，重写实验报告与项目完成报告：按项目目标、系统设计、MongoDB 设计、跳转设计、校验设计、AI 使用过程、测试结果、遇到的问题、如何解决重新组织；补充 27 个路由、四个集合字段与索引、跳转运行算法与边界、三层校验及 min/max/exact 语义；在 AI 使用部分明确区分 AI 生成、AI 初版问题和本人局部修正，补充本人负责的总体设计、数据模型、状态机、跳转规则、校验体系、配置交互、填写流程、统计与验收标准；将测试结果同步为 71 个用例全部通过，修正完成率文档口径为已提交/已开始，并更新 README 文档说明；用户要求撰写包含 AI 帮助、AI 失误、本人修改和本人设计的实验报告，并补充本人主导的设计与验收性微调说明


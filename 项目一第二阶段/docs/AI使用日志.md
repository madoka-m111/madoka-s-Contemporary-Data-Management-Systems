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


## 2026-10-22，使用记录69，read，大作业一：需求变更.docx、docs/项目完成报告.md、docs/数据库设计.md，通读第二阶段需求变更，把 8 项需求拆成可验收的功能点：题目可保存并重复使用、题目可共享、已发布问卷中的题目不可修改、题目修改要留历史、旧版本可恢复、不同问卷可并存不同版本、可查看题目被哪些问卷使用、可对单题做跨问卷统计；同时对照第一阶段报告确认原有四集合、问卷状态机、填写与统计接口不能被破坏。用户要求先理解需求变更，不要直接推翻第一阶段实现，并说明哪些旧功能必须保持兼容。

## 2026-10-22，使用记录70，read，app/models/user.py、app/models/survey.py、app/models/question.py、app/models/response.py、app/services/survey_service.py、app/services/question_service.py、app/routes/survey_routes.py、tests/conftest.py，盘点第一阶段的数据归属和调用链：题目原先直接属于某份问卷，题目内容与跳转逻辑都保存在 questions 集合中，统计按 survey_id 查询 responses；问卷发布只改变 status，未记录发布时刻，因此无法判断发布后题目是否被改过。用户要求在不改坏旧接口的前提下，为“题目复用”和“发布后不可变”找到最小侵入的改造点。

## 2026-10-22，使用记录71，design，docs/数据库设计.md，确定第二阶段的领域模型：将“题目身份”和“题目内容版本”分离，question_families 只保存稳定身份、作者、共享人、最新版本指针；question_versions 保存每次修改的不可变内容及 parent_version_id、restored_from_version_id、derived_from_version_id；问卷中的 questions 不改为引用，而是继续保存一份内容快照，并记录 bank_family_id、bank_question_id、bank_version，从而保证题库改题不会影响旧问卷。用户要求既要支持版本并存，又要保证旧问卷内容绝对不变。

## 2026-10-22，使用记录72，write，app/models/question_bank.py，实现 QuestionFamily 与 QuestionVersion 两个模型：QuestionFamily 提供 owner_id、title、latest_version_id、shared_with、is_public、version_count 以及 save/find_by_id/update/delete；QuestionVersion 提供 family_id、version_number、title、description、type、options、required、validation、jump_logic、change_note、parent_version_id、restored_from_version_id、created_by、created_at，并提供按 family 查询、取最新版本、计算下一版本号等方法。用户要求题目本身可以改，但历史版本不能被覆盖。

## 2026-10-22，使用记录73，write，app/models/question_bank.py，实现 QuestionBank 与 QuestionBankEntry 模型：题库支持 owner_id、name、description、is_default，提供按所有者查询、重命名、删除；题库条目使用 bank_id + family_id 唯一关联，支持加入、查找、移出、按题库删除条目。默认题库由服务层按用户自动创建，自定义题库可建多个，同一道题可以加入不同用户的题库。用户要求题库本身也要能管理，而不是只做一个全局题目列表。

## 2026-10-22，使用记录74，edit，app/models/question.py、app/__init__.py，扩展问卷内题目快照字段：新增 bank_family_id、bank_question_id、bank_version，并保持原有 survey_id、order、type、options、validation、jump_logic 等字段不变；在应用工厂中绑定四个新集合，为 question_families 的 owner_id/shared_with/is_public、question_versions 的 family_id+version_number 唯一索引、question_banks 的 owner_id+name 唯一索引、question_bank_entries 的 bank_id+family_id 唯一索引创建索引，同时给 questions 的 bank_family_id、bank_question_id 建普通索引。用户要求新功能可直接在现有 MongoDB 上增量部署，不需要迁移旧数据。

## 2026-10-22，使用记录75，write，app/services/question_bank_service.py，实现题库建题主流程：create_question 先创建 QuestionFamily，再创建 v1 QuestionVersion，把版本内容写入版本集合，更新 family 的 latest_version_id 和 version_count，最后把题目加入默认题库或指定题库；创建时校验标题、题型和选项，题目身份与版本内容分离，后续问卷选题只读取版本快照。用户要求“新建一道题并保存下来，以后做新问卷可以直接选”。

## 2026-10-22，使用记录76，edit，app/services/question_bank_service.py，实现“修改题目即生成新版本”：update_question 不覆盖原版本，而是读取当前或指定 base_version_id，计算下一版本号，复制题目内容后再应用本次修改，写入 parent_version_id 和 change_note，并更新 family 的最新版本指针；支持从任意历史版本继续派生，从而允许不同问卷使用不同代际的题目内容。用户要求每次改题都能追溯“从哪一版改来”，并且旧版本不能消失。

## 2026-10-22，使用记录77，edit，app/services/question_bank_service.py，实现版本历史与恢复：get_history 按 version_number 倒序返回某题的所有版本，并标记 is_latest、parent_version_id、restored_from_version_id；restore_version 读取指定历史版本内容，生成一个新的恢复版本，记录 restored_from_version_id 和恢复说明，而不是把最新指针直接拨回旧版本，从而保留“何时恢复、从哪版恢复”的完整链路。用户要求能看到题目改过几次，并能把旧版本恢复出来继续使用。

## 2026-10-22，使用记录78，edit，app/services/question_bank_service.py，实现题目共享：share_question 校验目标用户名存在且不能共享给自己，将目标用户加入 family.shared_with；unshare_question 支持取消共享；can_view 统一判断所有者、共享人、公开题三种可见性；列表接口按 scope=all/mine/shared/public 返回不同范围。共享只授予“查看和引用”能力，不授予修改原题能力，避免被共享者改动作者题库。用户要求题目可以共享给其他用户，同时原题仍由作者控制。

## 2026-10-22，使用记录79，edit，app/services/question_bank_service.py，实现公开题与派生副本：set_public 控制 family.is_public，公开后其他登录用户可在公开范围检索和引用；fork_question 让被共享者或公开题使用者复制出一个属于自己的新 family，新 family 的 v1 指向原版本并记录 derived_from_version_id，后续修改只影响自己的副本。用户要求别人可以基于我的题做自己的版本，但不能直接改我的题。

## 2026-10-22，使用记录80，edit，app/services/question_bank_service.py，实现题库管理：get_or_create_default_bank 保证每个用户首次进入题库时自动拥有“我的题库”，list_banks 返回题库及题目数量，create_bank/update_bank/delete_bank 支持新建、改名、删除自定义题库；默认题库禁止删除，删除自定义题库时同步清理条目，但不会删除题目 family 和 version。用户要求题库可以分组管理，并避免误删默认题库导致题目丢失。

## 2026-10-22，使用记录81，edit，app/services/question_bank_service.py，实现题库条目管理：add_to_bank 校验题库归属和题目可见性，使用 bank_id+family_id 唯一关联避免重复加入；remove_from_bank 支持从题库移出；list_bank_questions 返回题库内题目的最新版本信息，并兼容 scope 过滤；list_families 支持按作者、共享、公开范围查询。用户要求可以把题目加入不同题库，也可以从题库移出，但移出题库不等于删除题目。

## 2026-10-22，使用记录82，edit，app/services/question_bank_service.py，实现“题目使用情况”查询 get_usage：按 bank_family_id 在 questions 集合中反查所有引用该题身份的问卷内题目，关联 survey 得到标题、状态、作者，返回问卷 id、题目快照 id、使用版本号、是否最新版本和该问卷已提交回答数；非作者查询时只保留自己创建的问卷，避免通过共享题目读取他人答卷元数据。用户要求修改题目之前能知道哪些问卷正在使用它。

## 2026-10-22，使用记录83，edit，app/services/stats_service.py，实现跨问卷单题统计 get_family_stats：先按 family_id 找到所有使用该题的问卷内题目快照，再按 survey_id 和 status=submitted 读取 responses；输出 overall 汇总、per_version 按版本统计、per_survey 按问卷统计三部分，并返回使用问卷数、总回答数、各版本使用次数。不同问卷使用不同版本时，统计既不会混为一谈，也能给出总体分布。用户要求查看“你的年龄”这类题在所有问卷里的总体情况。

## 2026-10-22，使用记录84，edit，app/services/stats_service.py，细化跨问卷统计的题型处理：单选、多选、下拉统计各选项人数和百分比；评分、数字、滑块统计均值、最值、中位数和数值分布；文本题返回回答样本及数量；日期题统计日期分布；文件题只返回回答数；一份回答同时命中多个版本快照时只计一次总回答数，避免 overall 回答数被重复累加；题型混合时按题型分组输出。用户要求选择题看分布，数字题看均值和范围，文本题能看具体回答。

## 2026-10-22，使用记录85，edit，app/services/stats_service.py、app/services/question_bank_service.py，补全统计权限：题目作者可以查看该题在所有使用问卷中的汇总；被共享者只能查看自己创建的问卷；无权查看者返回 404 而不是泄露题目是否存在；get_usage 与 get_family_stats 共用同一套可见性判断。用户要求共享题目后既能协作，又不能借统计接口读取别人的答卷。

## 2026-10-22，使用记录86，edit，app/services/question_service.py，实现从题库添加单题 add_question_from_bank：先通过 QuestionBankService 取指定版本并校验用户可见性，再把版本中的标题、描述、题型、选项、必填、校验规则、跳转逻辑复制到 questions 快照，写入 bank_family_id、bank_question_id、bank_version，题目顺序排在当前问卷末尾；接口既支持传最新版本，也支持传历史版本 id。用户要求做新问卷时能直接从题库选一道题，且不同问卷可以使用不同版本。

## 2026-10-22，使用记录87，edit，app/services/question_service.py，实现批量从题库加题 batch_add_questions_from_bank：先遍历全部题目做存在性、可见性和版本校验，全部通过后再统一写入，避免中途某题无权使用导致前面题目已经写入、形成半批数据；批量写入时按传入顺序递增 order，并复用单题的快照复制逻辑。用户要求一次选择多道题库题时要么全部成功，要么全部不写入。

## 2026-10-22，使用记录88，edit，app/services/question_service.py、app/models/survey.py，实现“已发布问卷题目不可变”：在 Survey 模型中补充 published_at 并在发布时写入，QuestionService 新增 _questions_editable 判断，统一拦截 add_question、batch_add_questions、add_question_from_bank、batch_add_questions_from_bank、update_question、delete_question、reorder_questions；判断只看 published_at 是否存在，因此问卷撤回为草稿后题目仍然锁定，防止已收集答卷与题目内容不一致。用户要求问卷一旦发布，里面的题目不能再改，旧问卷必须保持原样。

## 2026-10-22，使用记录89，edit，app/services/survey_service.py，实现“复制为新版本” duplicate_survey：复制问卷基础信息生成新草稿，逐题复制题目内容并建立旧题目 id 到新题目 id 的映射，再重写 jump_logic 中的源题目和目标题目引用，避免副本跳转到旧问卷；副本不继承 published_at，因此可以继续编辑。用户要求已发布问卷不能直接改题时，可以复制出一份新问卷继续修改，同时旧问卷和旧答卷不受影响。

## 2026-10-22，使用记录90，write，app/routes/question_bank_routes.py，新增题目库核心 REST 路由：题目列表/新建/详情/修改、显式创建新版本、派生副本；family 的版本历史、恢复、共享、取消共享、公开范围；使用情况与跨问卷统计；题库列表/新建/修改/删除、题库内题目列表、加入题库、移出题库。所有路由统一使用 JWT 身份，服务层返回的错误转换为 400/403/404 和统一响应格式。用户要求把第二阶段的服务能力完整暴露为可调用的 API。

## 2026-10-22，使用记录91，edit，app/routes/question_bank_routes.py，补齐路由别名与边界处理：增加 `/questions/<version_id>/history|usage|stats` 别名，便于前端只拿到版本 id 时直接查询；恢复版本、移除题库题等接口补上成功返回；加入题库同时接受 family_id 或 question_id/version_id；对非法分页、空标题、无效版本 id 统一返回明确错误，避免 500。用户要求 API 既要好用，也要在参数缺失或非法时给出可理解的提示。

## 2026-10-22，使用记录92，edit，app/routes/survey_routes.py，接入问卷侧新接口：新增 `POST /surveys/<id>/questions/from-bank` 单题选题、`POST /surveys/<id>/questions/from-bank/batch` 批量选题、`POST /surveys/<id>/duplicate` 复制问卷；原有 `POST /questions` 和批量加题接口在检测到 bank_question_id 或 version_id 时自动走题库快照逻辑，未传时仍走第一阶段的手工建题逻辑，保证旧前端和旧测试不受影响。用户要求题库功能接入现有问卷接口，同时不改变第一阶段调用方式。

## 2026-10-22，使用记录93，write，frontend/question_bank.html，搭建题目库管理页结构：顶部工具栏放搜索框、范围筛选和新建题目；左侧显示题库列表和新建题库入口；主区显示题目卡片，包含题型、标题、作者、版本号、使用问卷数和操作按钮；页面下方用弹窗承载版本历史、使用情况、跨问卷统计等较重的信息，避免主列表过度拥挤。用户要求有一个独立页面集中管理题目库，而不是把功能塞进问卷编辑页。

## 2026-10-22，使用记录94，edit，frontend/question_bank.html，实现题库管理交互：加载题库列表、切换当前题库、按名称搜索、按“全部可用/我的题目/共享给我/公开题目/当前题库”切换范围；新建题目时提交标题、题型、选项、必填和校验配置；新题库可创建，题目可加入当前题库或从当前题库移出；未选择题库时显示引导而不是空白页。用户要求题库页能完成日常的建题、分类和查找操作。

## 2026-10-22，使用记录95，edit，frontend/question_bank.html，实现题目卡片上的版本与协作操作：点击“版本历史”显示每一版的版本号、修改说明、是否最新、父版本和恢复按钮；点击“使用情况”显示问卷标题、状态、使用版本和回答数；点击“跨问卷统计”展示总体、按版本、按问卷三组数据；支持输入用户名共享、取消共享、公开/取消公开、派生自己的副本。用户要求不用看数据库也能知道题目被谁使用、改过几次、总体答案是什么。

## 2026-10-22，使用记录96，edit，frontend/dashboard.html，把第二阶段入口接到问卷列表：侧边栏增加“题目库管理”，每份问卷增加“复制为新版本”操作，已发布问卷仍保留“填写链接/统计”等旧功能；复制成功后刷新列表并提示新草稿已生成，用户可以直接进入副本编辑。用户要求从主页就能进入题库和复制已发布问卷，不需要记额外地址。

## 2026-10-22，使用记录97，edit，frontend/create.html，在创建问卷页加入“从题库添加题目”弹窗：打开时拉取可用题目，展示题目标题、题型、作者、最新版本和历史版本；支持选择最新版或指定历史版本，支持多选后一次性加入本地题目列表；加入后在题目卡片显示“题库 vX”来源；保存整份问卷时优先调用批量 from-bank 接口，避免本地临时题目与题库版本脱节。用户要求创建问卷时能直接复用题库题目，并能明确选择使用哪一版。

## 2026-10-22，使用记录98，edit，frontend/edit.html，在编辑问卷页加入同样的题库选题弹窗，并补充只读锁定：已发布问卷或曾发布后撤回的问卷显示“题目已锁定”，隐藏或禁用新增、编辑、删除、排序、题库选题等入口；题目卡片显示“题库 vX”来源，普通草稿仍可正常编辑；页面加载时读取 questions_locked，而不是只根据当前 status 判断。用户要求编辑页能复用题库，同时不能让用户误以为已发布问卷还能改题。

## 2026-10-22，使用记录99，edit，frontend/create.html、frontend/edit.html，补齐 9 种题型在第二阶段的兼容：单选、多选、下拉、文本、数字、评分、日期、文件、滑块在创建和编辑页都能正确渲染选项、必填、校验条件和跳转配置；从题库复制过来的 validation/jump_logic 要能回填，保存时不能被临时字段污染。用户要求题库题目不只支持单选题，第一阶段已有题型在新流程中都要能正常使用。

## 2026-10-22，使用记录100，write，tests/test_question_bank.py，搭建第二阶段测试基础设施：使用 mongomock 初始化应用和数据库，封装 _make_user、_create_survey、_create_bank_question、_add_from_bank、_publish、_submit 等辅助函数，让每个测试都能独立创建用户、问卷、题库题、发布和提交回答，不依赖真实 MongoDB。用户要求新增测试必须能稳定运行，并且不破坏第一阶段测试环境。

## 2026-10-22，使用记录101，edit，tests/test_question_bank.py，编写版本与恢复测试 test_bank_question_versions_history_and_restore：创建题目后校验 v1，连续修改两次校验 v2、v3 和 parent_version_id，再恢复 v1，断言版本数增加、最新版本内容回到 v1、restored_from_version_id 指向 v1，并且旧版本仍然存在。用户要求用自动化测试证明修改不会覆盖历史、恢复旧版本也不会丢掉新版本。

## 2026-10-22，使用记录102，edit，tests/test_question_bank.py，编写多问卷快照测试 test_question_snapshot_is_shared_by_multiple_surveys：同一道题库题分别加入两份问卷，把题库题改到 v2 后重新读取两份问卷，断言两份问卷的题目标题仍是加入时的内容、bank_version 分别记录当时的版本，证明题库修改只影响后续选题，不会回写旧问卷。用户要求验证“一个题目可以被多个问卷使用，且旧问卷不被影响”。

## 2026-10-22，使用记录103，edit，tests/test_question_bank.py，编写发布锁定与复制测试 test_published_survey_question_is_immutable_and_can_be_duplicated：发布问卷后分别调用修改、删除、新增、排序接口，断言全部返回失败；撤回后再次尝试修改仍失败；调用 duplicate 后断言新问卷是草稿、题目数量一致、题目 id 已重新生成且 jump_logic 引用已重写。用户要求验证已发布题目不可变，同时提供可继续编辑的副本。

## 2026-10-22，使用记录104，edit，tests/test_question_bank.py，编写共享与公开测试：test_share_question_and_fork 验证共享后对方能查看、能派生副本、不能直接改原题，取消共享后不可见；test_public_question_and_batch_add_from_bank 验证公开题可被其他用户批量加入问卷；test_private_question_cannot_be_used_by_other_user 验证私有题被他人引用时返回失败。用户要求共享是可控的，公开和私有必须有明确边界。

## 2026-10-22，使用记录105，edit，tests/test_question_bank.py，编写统计与题库测试：test_cross_survey_stats_aggregates_versions 用两份问卷分别引用 v1/v2 并提交回答，断言总体回答数、按版本统计和按问卷统计都正确；test_bank_management_add_remove_and_default 验证默认题库自动创建、加入移出题目、默认题库不可删除；test_shared_question_stats_only_include_own_surveys 验证被共享者只能统计自己创建的问卷。用户要求用测试固定跨问卷统计口径和题库管理边界。

## 2026-10-22，使用记录106，edit，app/services/question_service.py、app/routes/question_bank_routes.py、frontend/question_bank.html，集中修复第二阶段回归问题：批量从题库加题改为先整体校验再写入，避免半批数据；恢复版本、移出题库等路由补齐返回值，避免前端拿到空响应；题库页修正“全部可用/当前题库”切换后列表不刷新、空题库时误显示全部题目的问题；对已发布问卷的锁定提示统一走 questions_locked。用户要求功能不仅要能跑通，还要在失败和边界场景下表现正确。

## 2026-10-22，使用记录107，edit，docs/数据库设计.md，补充第二阶段数据库设计：新增 question_families、question_versions、question_banks、question_bank_entries 四个集合的字段、索引、关系说明；记录 questions 新增的 bank_family_id、bank_question_id、bank_version 快照字段；明确“family 是身份、version 不可变、entry 是题库关联、question 是问卷快照”的一致性规则，以及题库改题不更新旧问卷、发布后题目锁定、恢复生成新版本等约束。用户要求数据库文档能解释新增集合为什么这样设计，而不是只列字段。



## 2026-10-22，使用记录108，edit，frontend/question_bank.html，为题库新建/编辑题目弹窗补齐限制条件：新增与创建问卷页一致的“⚙ 限制条件”卡片、限制摘要、清除按钮和题型提示；根据题型动态提供多选题最少/最多/必须选择数、文本题与多行文本题最少/最多字数、数字题最小值/最大值/仅允许整数；切换题型时清空不适用的旧限制，保存题目时由前端统一校验数量、字数、范围与互斥规则，并把 `validation` 随 `POST /question-bank/questions` 或 `PUT /question-bank/questions/<id>` 提交；题目列表的标签区展示已配置的限制摘要；内联 JavaScript 通过 `node --check`，用轻量 DOM 桩验证三种题型的渲染、读取、摘要与校验分支，pytest 80 passed；用户要求题库的新建题目页面也能像创建问卷一样，按所选题型填写对应的限制条件，并保持相同样式

## 2026-10-22，使用记录109，edit，frontend/question_bank.html、tests/test_question_bank.py，修复“共享后对方看不到共享题”的显示问题：确认后端按题目共享本身正常，根因是题库页默认选中某个题库并调用题库内题目接口，导致上方“共享给我的”范围筛选被忽略；现在页面默认进入“全部可用题目”，切换范围时自动退出当前题库并退出高亮，题库模式下范围框显示“当前题库”，并补充“共享是按单道题目共享、不会自动进入对方题库”的空状态和使用说明；同时增加后端回归断言，验证 scope=all 包含共享题、被共享者默认题库不会自动出现共享题；node --check 与范围切换 DOM 桩通过，pytest 80 passed；用户要求查清把题库共享给其他账户后对方收不到共享题的原因并修正

## 2026-10-26，使用记录110，edit，docs/测试用例.md，修正测试用例文档与实际 pytest 收集数不一致的问题：原文档只统计前 8 个测试文件共 71 个用例，漏掉 test_question_bank.py 的 9 个题库测试；新增“9. 题库管理测试”章节，逐条记录版本历史与恢复、问卷快照隔离、已发布题目锁定与问卷复制、共享与派生、跨问卷统计、题库管理、共享统计权限、公开题批量加入、私有题权限共 9 个用例，并补充 2.7 无效问卷 ID 用例；测试总计由 71 更新为 80，新增说明“用例数按 pytest 收集的测试函数统计，个别小节合并多个测试函数”；实际运行 pytest 为 80 passed；用户要求解释文档仍写 71 个测试而实际为 80 个，并同步修正文档


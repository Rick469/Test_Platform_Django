# Test_Platform_Django

一. 框架架构

  使用Python+Django+HTML+JS;
  
  使用Python编程语言；
  
  使用Django web开发框架；
  
  使用HTML+JS编写前端页面；

  
 二. 目录介绍
 
  1.guest
    
    settings.py
      
      全局项目配置文件，主要配置数据库地址等；
      
    urls.py
    
      url路径文件，映射url和views函数；
   
  2.sign
  
    API_Test
    
      接口测试平台文件目录，主要自动生成Python测试用例脚本文件；
      
     config
     
      接口测试环境以及路径配置；
      
     migrations
      
      执行数据库迁移自动生成的迁移记录文件；
      
     static
      
      项目静态文件目录，放置接口测试报告、Excel用例文件、Excel模板文件等
      
     templates
      
      项目HTNL前端页面文件；
      
     models.py
      
      数据库表结构文件；
      
     views.py
     
      后端处理函数文件；
      
     test_tools.py
     
      测试工具应用对应处理函数文件；
    
 三. 框架执行
 
  在根目录下执行cmd: python runserver 0.0.0.0:8000

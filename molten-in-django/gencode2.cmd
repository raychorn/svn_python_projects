@echo off


sqlautocode -t app_setting,article,case_columns_setting,case_report,case_view_setting,country,error,page,rails_cron,rating,refresh_cache,schema_info,sfaccount,sfattach,sfcase,sfcase_watcher,sfcase_watcher_list,sfcatdata,sfcatnode,sfccomment,sfcomponent,sfcontact,sfcontact_setting,sfcontactcopy,sfgroup,sfmolten_post,sfproduct_team,sfsolution,sfsolution_setting,sfssl,sfuser,solution_relevancy,solution_search_log,tip,viewing mysql://root:peekab00@localhost:3306/molten_development -o molten_tables.py

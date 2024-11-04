temp_query = '''
            SELECT * 
            FROM homerseklet
            WHERE hutopanel_id = ? AND adag_id = ?        
        '''

portion_query = '''
            SELECT DISTINCT adag_id, start_datetime, end_datetime
            FROM adagok
        '''

panel_query = '''
        SELECT * 
        FROM hutopanelek
    '''

panel_query = '''
            SELECT h.*, a.*
            FROM homerseklet h
            JOIN adagok a ON h.adag_id = a.adag_id
            WHERE h.adag_id = ? AND a.idotartam < 120 AND h.hutopanel_id = ?  
        '''

two_panel_query = '''
            SELECT h.*, a.*
            FROM homerseklet h
            JOIN adagok a ON h.adag_id = a.adag_id
            WHERE h.adag_id = ? AND a.idotartam < 120 AND h.hutopanel_id = ?    
        
            UNION
        
            SELECT h.*, a.*
            FROM homerseklet h
            JOIN adagok a ON h.adag_id = a.adag_id
            WHERE h.adag_id = ? AND a.idotartam < 120 AND h.hutopanel_id = ?   
        '''

all_panel_query = '''
            SELECT h.*, a.*
            FROM homerseklet h
            JOIN adagok a ON h.adag_id = a.adag_id
            WHERE h.adag_id = ? AND a.idotartam < 120 
        '''
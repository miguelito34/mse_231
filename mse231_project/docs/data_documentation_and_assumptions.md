# Data Documentation and Assumptions

* __Variable Names for data_calls__
	* __city__: city that the 311 data is pulled from
	* __status__: labeled "closed" if the 311 request has been dealt with, open otherwise
	* __srvc_nm__: raw service name as given from Open311
	* __address__: raw adress of the request as given from Open311
	* __req_dt__: the date and time the request was requested by the user
	* __updt_dt__: the date and time of the most recent user; if status is "closed", this is the closed date and time
	* __fix_min__: total minutes it took to close the request; only calculated for "closed" requests.
	* __geoid__: the census geoid for the state, county, and census tract the call falls within
	* __topic__: the umbrella topic that the team has assigned to the call; 20 in total
	* __req_aim__: the aim of the request; human if it is targeted at a human, their belongings, their actions, or their property: non-human otherwise
	* __illegal__: whether or not the request may involve something potentially illegal
	* __adv__: whether or not the request is adversarial towards a human, their belongings, their actions, or their property

* __Variable Names for data_descriptive__
	* __geoid__: the census geoid for the state, county, and census tract the call falls within
	* __detail__: the state, county, and census tract the call falls within (in words)
	* __st_fip__: the state census FIP code, also the first two numbers in the geoid
	* __cty_fip__: the county census FIP code, also the 3-5 numbers in the geoid
	* __trt_fip__: the census tract FIP code, also the last 6 numbers in the geoid
	* __state__: the state that the call falls within
	
	* __POPULATION ASSUMPTIONS AND NOTES__:
		* The Census data used is from 2015
		* `pop_wht` and `pop_nw` sum to 1
		* Employment statistics are for those 16 and older
		* Education statistics are for those 25 and older
	* __pop_tot__: the total population (ie number of people) of the census tract
	* __pop_wht__: proportion of the total population White alone (non-hispanic)
	* __pop_nw__: proportion of the total population non-white alone
	* __pop_blk__: proportion of the total population Black alone (non-hispanic)
	* __pop_his__: proportion ofthe total Hispanic population
	* __pop_asi__: proportion of the total population Asian alone (non-hispanic)
	* __pop_two__: proportion of the total population that is two or more races (non-hispanic)
	* __pop_oth__: proportion of the total population some other race alone (non-hispanic)
	* __pop_nat__: proportion of the total population American Indian and Alaska Native alone (non-hispanic)
	* __pop_isl__: proportion of the total population Native Hawaiian and Other Pacific Islander alone (non-hispanic)
 	* __emp_une__: total proportion of those in the labor force (including armed services) that are unemployed
 	* __emp_emp__: total proportion of those in the labor force (including armed services) that are employed
 	* __ed_grad__: the total proportion of the population with either a masters, professional degree, or PhD
 	* __ed_bs__: the total proportion of the population with a bachelors
 	* __ed_as__: the total proportion of the population with an associates
 	* __ed_hs__: the total proportion of the population with a high school degree or equivalent
 	* __ed_l_hs__: the total proportion of the population with less than a high school degree; also 1 - (ed_grad + ed_bs + ed_as + ed_hs)
 	* __med_inc__: median household income in the past 12 months
 	* __med_val__: median value (in $) of owner occupied units
 	* __med_ren__: median rent (in $) of owner occupied units paying rent
 	* __geometry__: the census tract shapefile
    # def get_its_dates(self, company_id: int, service_id: int, max_amount: int = -1):
    #     """
    #     Получает доступные даты и время записи для данного мастера.

    #     Args:
    #         company_id (int): Идентификатор компании.
    #         service_id (int): Идентификатор услуги.
    #         max_amount (int): Максимальное количество дат, которое нужно загрузить (-1 для загрузки всех).

    #     Returns:
    #         list[Dates]: Список объектов Dates с датами и временем доступности мастера.
    #     """
    #     URL = "{base_url}/get_datetimes/?company_id={company_id}&service_id[]={service_id}&master_id={master_id}&with_first=1"
    #     result_url = URL.format(base_url=DikidiApi.URL, company_id=company_id, service_id=service_id, master_id=self.id)
    #     logger.debug(f"URL для получения дат записи мастера (master_id={self.id}): {result_url}")

    #     json_data = DikidiApi.get_data_from_api(result_url)
    #     if not json_data:
    #         logger.warning(f"Нет данных о доступных датах для мастера {self.id}")
    #         return []

    #     all_dates = json_data.get("dates_true", [])

    #     if max_amount != -1:
    #         all_dates = all_dates[:max_amount]

    #     for date in all_dates:
    #         self.dates.append(
    #             Date(
    #                 date_string=date, 
    #                 times=[]
    #             )
    #         )

    #     return self.dates
# @inject
# async def save_manager_in_redis_db(
#         callback_query: types.CallbackQuery,
#         callback_data: dict,
#         state: FSMContext,
#         redis: Redis = Provide[Container.redis],
#         order_service: OrderService = Provide[Container.order_service],
#         image_service: ImagesService = Provide[Container.images_service],
#         report_service: ReportService = Provide[Container.report_service],
#         keyboard_service: FormInlineKeyboardService = Provide[Container.keyboard_service],
#         validate_service: ValidateInformationService = Provide[Container.validate_service]
#
# ):
#     user_id = callback_query.from_user.id
#     data = callback_data.get("data")
#     check_value = await redis.check_value(user_id=user_id)
#
#     if not data.isdigit() and data != "next" and data != "all_managers":
#         await callback_query.message.edit_reply_markup()
#         if check_value:
#             await redis.remove_value(user_id=user_id)
#
#         if data == "back_button":
#             await ViewOrderOrReportFilter.type_date.set()
#             await callback_query.message.answer("Возращаемся к педыдущему шагу⏪")
#             await callback_query.message.answer(
#                 "Выберите промежуток за который хотите просмотреть заказы: ",
#                 reply_markup=date_keyboard
#             )
#
#         else:
#             await callback_query.message.answer("Действия отменены❌")
#             return await state.finish()
#
#     else:
#         await callback_query.message.edit_reply_markup()
#         if not check_value and data != "all_managers":
#             await callback_query.message.answer("Чтобы продолжить выберите определенных менеджеров,"
#                                                 " либо отмените действие, либо вернитесь на шаг назад")
#         else:
#             managers = await redis.get_value(user_id=user_id)
#             clear_manager_list = await validate_service.delete_copy_manager_id(managers=managers)
#             await redis.remove_value(user_id=user_id)
#             async with state.proxy() as data_state:
#                 date = data_state.get("date")
#                 type_view = data_state.get("view_type")
#                 start_date = data_state.get("date_start")
#                 end_date = data_state.get("date_end")
#                 if date:
#                     if type_view == "report":
#                         if data == "all_managers":
#                             reports = await report_service.get_report_with_all_managers(date=date)
#                             for report in reports:
#                                 await callback_query.message.answer(
#                                     f"{hbold('Отчет:')}\n\n"
#                                     f"{report.report}\n"
#                                     f"{hbold('Менеджер')}:  {report.user.last_name}\n"
#                                     f"{hbold('Создан')}:  {report.created_at}",
#                                     reply_markup=await keyboard_service.report_keyboard(
#                                         report_id=report.id
#                                     ))
#                 else:
#                     pass
#
#     if not check_value and data.isdigit():
#         logger.info("Создали")
#         await redis.insert_value(
#             user_id=user_id,
#             value=data
#         )
#
#     elif data.isdigit():
#         logger.info("Добавили")
#         await redis.append_value(
#             user_id=user_id,
#             value=data
#         )

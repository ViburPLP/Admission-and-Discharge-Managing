# from django.shortcuts import redirect

# class RoleRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     # def __call__(self, request):
#     #     user = request.user
#     #     if not user.is_authenticated:
#     #         return redirect('login')
#     #     if request.path.startswith(('/pending_admissions/', 
#     #             '/admitting_member_detail/',
#     #             '/discharging_member_detail/',
#     #             '/trend-analysis/',
#     #             '/admit_member/',
#     #             '/discharge_member/',
#     #             '/admission_history/',
#     #             '/generate_admission_report/',
#     #             '/currently_admitted/',
#     #             )
#     #               ) and not user.groups.filter(name='Claims Managers').exists():
#     #         return redirect('login')
#     #     response = self.get_response(request)
#     #     return response

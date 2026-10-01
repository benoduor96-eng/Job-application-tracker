"""HTTP endpoints for the job-search planning workspace."""
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from apps.jobs.search_planner import JobSearchPlanner

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def planning_summary(request):
    return JsonResponse(JobSearchPlanner(request.user).summary())

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def planning_queue(request):
    try: limit=int(request.GET.get("limit","12"))
    except ValueError: return JsonResponse({"detail":"limit must be an integer"},status=400)
    if not 1<=limit<=50: return JsonResponse({"detail":"limit must be between 1 and 50"},status=400)
    items=JobSearchPlanner(request.user).daily_plan(limit)
    return JsonResponse({"items":[x.to_dict() for x in items],"count":len(items)})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def planning_quality(request):
    rows=JobSearchPlanner(request.user).application_quality()
    return JsonResponse({"applications":rows,"average_score":round(sum(x["score"] for x in rows)/len(rows),2) if rows else 0})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def planning_capacity(request):
    try:
        applications=int(request.GET.get("applications","10"))
        followups=int(request.GET.get("followups","5"))
    except ValueError:
        return JsonResponse({"detail":"targets must be integers"},status=400)
    if not 0<=applications<=100 or not 0<=followups<=100:
        return JsonResponse({"detail":"targets must be between 0 and 100"},status=400)
    return JsonResponse(JobSearchPlanner(request.user).weekly_capacity(applications,followups))

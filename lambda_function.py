# coding:utf-8
import json
import boto3
import datetime

def get_data(text,quota_client,servicecode,quotacode,cloudwatch_client,now,week_ago,url,message):
    quota = quota_client.get_service_quota(
        ServiceCode=servicecode,
        QuotaCode=quotacode
    )
    print(quota)
    # 現在の制限値
    limit = quota['Quota']['Value']
    print(limit)
    
    metrics = []
    for key, value in quota['Quota']['UsageMetric']['MetricDimensions'].items():
        metrics.append({'Name': key, 'Value': value})
    
    # 1時間間隔のメトリクスを取得。
    response = cloudwatch_client.get_metric_statistics(
        Namespace=quota['Quota']['UsageMetric']['MetricNamespace'],
        MetricName=quota['Quota']['UsageMetric']['MetricName'],
        Dimensions=metrics,
        StartTime=week_ago,
        EndTime=now,
        Period=3600,
        Statistics=['Maximum']
    )
    
    # 過去1週間で1時間ごとのメトリクス一覧
    print(response)
    
    list = []
    max_data = 0
    for data in response['Datapoints']:
        list.append(data['Maximum'])
    print(list)
    # メトリクスが存在すればメトリクス内の最大値を変数に代入
    if not list == []:
        max_data = max(list)
    print(max_data)
    
    # 閾値チェック
    if max_data > limit/2:
        print('上限緩和した方がいいかも')
        message += text
        message += '現在の制限値：' + str(limit) + '\n'
        message += '過去1週間の最大値：' + str(max_data) + '\n'
        message += '上限緩和の検討しましょう。\n'
        message += 'CloudWatchメトリクスのURLは以下となります。\n'  + url
    else:
        print('問題なし')
    
    # メール本文用文面を返す
    return message

def lambda_handler(event, context):
    # メール本文用変数
    message = ''
    
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    now_str = now.strftime("%Y-%m-%d")
    week_ago_str = week_ago.strftime("%Y-%m-%d")
    
    quota_client = boto3.client('service-quotas')
    cloudwatch_client = boto3.client('cloudwatch')
    
    print('Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances 用処理')
    # メール出すときにどのインスタンス群なのか明示する文章。
    text = 'Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances\n'
    # cloudwatchメトリクスのURL的なもの、アップデートとかで動かなくなる可能性あり。
    print("https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'Standard*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20Standard*20*28A*2c*20C*2c*20D*2c*20H*2c*20I*2c*20M*2c*20R*2c*20T*2c*20Z*29*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)")
    url = "https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'Standard*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20Standard*20*28A*2c*20C*2c*20D*2c*20H*2c*20I*2c*20M*2c*20R*2c*20T*2c*20Z*29*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)\n\n"
    message = get_data(text,quota_client,'ec2','quotacode',cloudwatch_client,now,week_ago,url,message)

    print('Running On-Demand F instances 用処理')
    # メール出すときにどのインスタンス群なのか明示する文章。
    text = 'Running On-Demand F instances\n'
    # cloudwatchメトリクスのURL的なもの、アップデートとかで動かなくなる可能性あり。
    print("https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'F*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20F*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)")
    url = "https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'F*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20F*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)\n\n"
    message = get_data(text,quota_client,'ec2','quotacode',cloudwatch_client,now,week_ago,url,message)

    print('Running On-Demand G instances 用処理')
    # メール出すときにどのインスタンス群なのか明示する文章。
    text = 'Running On-Demand G instances\n'
    # cloudwatchメトリクスのURL的なもの、アップデートとかで動かなくなる可能性あり。
    print("https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'G*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20G*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)")
    url = "https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'G*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20G*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)\n\n"
    message = get_data(text,quota_client,'ec2','quotacode',cloudwatch_client,now,week_ago,url,message)

    print('Running On-Demand P instances 用処理')
    # メール出すときにどのインスタンス群なのか明示する文章。
    text = 'Running On-Demand P instances\n'
    # cloudwatchメトリクスのURL的なもの、アップデートとかで動かなくなる可能性あり。
    print("https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'P*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20P*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)")
    url = "https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'P*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20P*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)\n\n"
    message = get_data(text,quota_client,'ec2','quotacode',cloudwatch_client,now,week_ago,url,message)

    print('Running On-Demand X instances 用処理')
    # メール出すときにどのインスタンス群なのか明示する文章。
    text = 'Running On-Demand X instances\n'
    # cloudwatchメトリクスのURL的なもの、アップデートとかで動かなくなる可能性あり。
    print("https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'X*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20X*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)")
    url = "https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#metricsV2:graph=~(metrics~(~(~'AWS*2fUsage~'ResourceCount~'Resource~'vCPU~'Service~'EC2~'Type~'Resource~'Class~'X*2fOnDemand))~period~300~stat~'Maximum~view~'timeSeries~stacked~false~title~'Running*20On-Demand*20X*20instances~region~'ap-northeast-1~start~'" + week_ago_str + "T03*3a00*3a00.999Z~end~'" + now_str + "T02*3a59*3a59.000Z)\n\n"
    message = get_data(text,quota_client,'ec2','quotacode',cloudwatch_client,now,week_ago,url,message)

    # 本文の内容が空でなければメールを送信
    if message:
        sns_client = boto3.client("sns")
        res = sns_client.publish(
            TopicArn=str('arn:aws:sns:ap-northeast-1:account-id:sns-name'),
            Message=str(message),
            Subject=str('vCPU-Test')
        )
        return(res)

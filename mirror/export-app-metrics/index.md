# Export app metrics

App metrics, which can be viewed in the [developer console](/platform/forge/view-app-metrics/),
show you how your Forge app is currently performing across all
[sites](/developer-guide/glossary).

You can also use our **App metrics API** to export app metrics to several observability tools,
including [SignalFX](https://www.splunk.com/) and [Datadog](https://www.datadoghq.com/).
Such tools offer capabilities, like grouping and filtering metrics by different attributes
and integrating with incident response tools.

The App metrics API is an [Atlassian GraphQL](/platform/atlassian-graphql-api/graphql/)
metrics API that provides metrics in the
[OTLP protobuf JSON](https://protobuf.dev/programming-guides/proto3/#json) format, which is
the format used in the
[OpenTelemetry framework](/platform/forge/app-metrics-in-third-party-tools/#opentelemetry-framework).

The following app metrics can be exported to monitoring tools via the App metrics API:

Exporting app metrics involves the following steps:

1. [Authenticate with the Atlassian GraphQL Gateway](#authenticate-with-the-atlassian-graphql-gateway/)
2. [Query the App metrics API](#query-the-app-metrics-api)
3. [Set up your infrastructure](#set-up-your-infrastructure)

Check out
[this repository](https://bitbucket.org/atlassian/forge-observability-consumption-patterns/src/main/metrics/)
for example code and resources for configuring observability tools
to consume Forge app metrics.

## Authenticate with the Atlassian GraphQL Gateway

You must first
[authenticate with the Atlassian GraphQL Gateway (AGG)](/platform/atlassian-graphql-api/graphql/#authentication)
to consume the API and export app metrics to a tool of your choice.

The Atlassian account making the request must be the same account that owns the Forge app.

To get started using basic authentication:

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Select **Create API token**.
3. Enter a label to describe your API token. For example, *export-metrics-api-token*.
4. Select **Create**.
5. Select **Copy to clipboard** and close the dialog.
6. Include the token and your email in the header of your GraphQL request.
7. Pass the `X-ExperimentalAPI` header. This is because the API is still in the experimental phase
   and is subject to change.
8. Provide a custom `User-Agent` header. This helps differentiate traffic coming from
   the developer console and your own export service. We recommend using this value:
   `ForgeMetricsExportServer/1.0.0`

## Query the App metrics API

You can use the *sample queries* below and try the App metrics API at
[GraphQL Gateway](https://api.atlassian.com/graphql) for your Forge app. Ensure to input
the corresponding *properties* in your queries.

* You can run a query for up to 14 days in the past. Each API call retrieves a maximum of 15 minutes
  of metrics. This limit is enforced to make sure there aren't too many data points returned
  in the API response.
* We recommend fetching data periodically, for example, every three or five minutes. A rate limit of
  five calls per minute per user is enforced.

### Sample queries

The sample queries return metrics in the
[OTLP protobuf JSON](https://protobuf.dev/programming-guides/proto3/#json) format, which is
the format used in the OpenTelemetry framework.

#### Sample AGG query

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
```



```
query Ecosystem($appId: ID!, $query: ForgeMetricsOtlpQueryInput!) {
  ecosystem {
    forgeMetrics(appId: $appId) {
      appMetrics(query: $query) {
        ... on ForgeMetricsOtlpData {
          resourceMetrics
        }
        ... on QueryError {
          message
          identifier
          extensions {
            statusCode
            errorType
          }
        }
      }
    }
  }
}
```
```

#### Sample AGG query variables

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
```



```
{
  "appId": "ari:cloud:ecosystem::app/8ce114f4-d82c-45e2-b4fb-c6a0751d7d57",
  "query": {
    "filters": {
      "environments": ["8cb293d5-be08-47ae-a75c-95b89da5ad1d"],
      "interval": {
        "start": "2023-06-18T02:55:00.000Z",
        "end": "2023-06-18T02:57:00.000Z"
      },
      "metrics": [
        "FORGE_API_REQUEST_COUNT", 
        "FORGE_API_REQUEST_LATENCY", 
        "FORGE_BACKEND_INVOCATION_LATENCY", 
        "FORGE_BACKEND_INVOCATION_COUNT", 
        "FORGE_BACKEND_INVOCATION_ERRORS", 
        "CONTAINER_CPU_USAGE_PERCENTAGE", 
        "CONTAINER_MEMORY_USAGE_PERCENTAGE", 
        "CONTAINER_UPTIME_SECONDS",
        "CONTAINER_STATUS_RESTARTS_TOTAL",
        "SERVICE_INSTANCE_COUNT"
      ]
    }
  }
}
```
```

```
```
1
2
3
4
5
6
```



```
{
  "Authorization": "Basic base64<email:token>",
  "User-Agent": "ForgeMetricsExportServer/1.0.0",
  "X-ExperimentalApi": "ForgeMetricsQuery"
}
```
```

#### Sample AGG query response

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
```



```
{
  "data": {
    "ecosystem": {
      "forgeMetrics": {
        "appMetrics": {
          "resourceMetrics": [
            {
              "resource": {},
              "schemaUrl": "https://opentelemetry.io/schemas/1.9.0",
              "scopeMetrics": [
                {
                  "metrics": [
                    {
                      "name": "forge_api_request_count",
                      "description": "",
                      "sum": {
                        "aggregationTemporality": 1,
                        "dataPoints": [
                          {
                            "asInt": 8,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "contextAri",
                                "value": {
                                  "stringValue": "ari:cloud:compass::site/04c5a385-0899-4edc-93a8-ada653b7c534"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "6f5f56e9-55c0-4551-9247-ee1484340f64"
                                }
                              },
                              {
                                "key": "provider",
                                "value": {
                                  "stringValue": "app"
                                }
                              },
                              {
                                "key": "remote",
                                "value": {
                                  "stringValue": "stargate"
                                }
                              },
                              {
                                "key": "status",
                                "value": {
                                  "stringValue": "2xx"
                                }
                              },
                              {
                                "key": "url",
                                "value": {
                                  "stringValue": "/forge/entities/graphql"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1698720840000000000",
                            "timeUnixNano": "1698720900000000000"
                          }
                        ]
                      },
                      "unit": "s"
                    },
                    {
                      "name": "forge_backend_invocation_count",
                      "description": "",
                      "sum": {
                        "aggregationTemporality": 1,
                        "dataPoints": [
                          {
                            "asInt": 70,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "8ce114f4-d82c-45e2-b4fb-c6a0751d7d57"
                                }
                              },
                              {
                                "key": "appVersion",
                                "value": {
                                  "stringValue": "4.64.0"
                                }
                              },
                              {
                                "key": "contextAri",
                                "value": {
                                  "stringValue": "ari:cloud:confluence::site/13095d29-407d-47ec-aa57-76764a470f36"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "functionKey",
                                "value": {
                                  "stringValue": "updateStatusTitle"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1687497375656000000",
                            "timeUnixNano": "1687497375662000000"
                          }
                        ]
                      },
                      "unit": "s"
                    },
                    {
                      "name": "forge_backend_invocation_errors",
                      "description": "",
                      "sum": {
                        "aggregationTemporality": 1,
                        "dataPoints": [
                          {
                            "asInt": 0,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "8ce114f4-d82c-45e2-b4fb-c6a0751d7d57"
                                }
                              },
                              {
                                "key": "appVersion",
                                "value": {
                                  "stringValue": "5.1.0"
                                }
                              },
                              {
                                "key": "contextAri",
                                "value": {
                                  "stringValue": "ari:cloud:compass::site/6a9ea14f-759d-4f4a-b3ac-11395d8bf519"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "errorType",
                                "value": {
                                  "stringValue": "UNHANDLED_EXCEPTION"
                                }
                              },
                              {
                                "key": "functionKey",
                                "value": {
                                  "stringValue": "process-app-event"
                                }
                              },
                              {
                                "key": "moduleKey",
                                "value": {
                                  "stringValue": "app-event-webtrigger"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1687488960000000000",
                            "timeUnixNano": "1687489020000000000"
                          }
                        ]
                      },
                      "unit": "s"
                    },
                    {
                      "name": "container_cpu_usage_percentage",
                      "description": "",
                      "gauge": {
                        "dataPoints": [
                          {
                            "asDouble": 1.121,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-8vg5v"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1687488960000000000",
                            "timeUnixNano": "1687489020000000000"
                          }
                        ]
                      },
                      "unit": "%"
                    },
                    {
                      "name": "container_memory_usage_percentage",
                      "description": "",
                      "gauge": {
                        "dataPoints": [
                          {
                            "asDouble": 21.7125,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-8vg5v"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1687488960000000000",
                            "timeUnixNano": "1687489020000000000"
                          }
                        ]
                      },
                      "unit": "%"
                    },
                    {
                      "name": "service_instance_count",
                      "description": "",
                      "gauge": {
                        "dataPoints": [
                          {
                            "asDouble": 2,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1687488960000000000",
                            "timeUnixNano": "1687489020000000000"
                          }
                        ]
                      },
                      "unit": "1"
                    },
                    {
                      "name": "container_uptime_seconds",
                      "description": "",
                      "gauge": {
                        "dataPoints": [
                          {
                            "asDouble": 388626.6037724018,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785240860000000000",
                            "timeUnixNano": "1785240920000000000"
                          },
                          {
                            "asDouble": 388626.60381031036,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-rhvk8"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785240860000000000",
                            "timeUnixNano": "1785240920000000000"
                          }
                        ]
                      },
                      "unit": "s"
                    },
                    {
                      "name": "container_status_restarts_total",
                      "description": "",
                      "sum": {
                        "aggregationTemporality": 2,
                        "isMonotonic": true,
                        "dataPoints": [
                          {
                            "asInt": 0,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785409740000000000",
                            "timeUnixNano": "1785409800000000000"
                          },
                          {
                            "asInt": 0,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785409800000000000",
                            "timeUnixNano": "1785409860000000000"
                          },
                          {
                            "asInt": 1,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785409800000000000",
                            "timeUnixNano": "1785409860000000000"
                          },
                          {
                            "asInt": 1,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785409800000000000",
                            "timeUnixNano": "1785409860000000000"
                          },
                          {
                            "asInt": 2,
                            "attributes": [
                              {
                                "key": "appId",
                                "value": {
                                  "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                }
                              },
                              {
                                "key": "cluster_uid",
                                "value": {
                                  "stringValue": "8ffs"
                                }
                              },
                              {
                                "key": "container",
                                "value": {
                                  "stringValue": "java-service-container-001"
                                }
                              },
                              {
                                "key": "environmentId",
                                "value": {
                                  "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                }
                              },
                              {
                                "key": "pod",
                                "value": {
                                  "stringValue": "eco-deployment-65db68664c-g5m2g"
                                }
                              },
                              {
                                "key": "region",
                                "value": {
                                  "stringValue": "us-west-2"
                                }
                              },
                              {
                                "key": "serviceKey",
                                "value": {
                                  "stringValue": "java-service"
                                }
                              }
                            ],
                            "startTimeUnixNano": "1785409800000000000",
                            "timeUnixNano": "1785409860000000000"
                          }
                        ]
                      },
                      "unit": "1"
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  }
}
```
```

### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `appId` | `string` | Yes | A unique identifier for your forge app which can be found in the app's `manifest.yml` file  *Regex:* `ari:cloud:ecosystem::app/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| `filters` | [Filters](#filters) | Yes | Filters to fetch metrics as required. See [Filters](#filters). |

#### Filters

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `environments` | `Array<string>` | Yes | A list of environment UUIDs for which metrics needs to be fetched. *Regex:* `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| `interval` | [Interval](#interval) | Yes | Time range for which metrics needs to be fetched. |
| `metrics` | `Array<enum>` | Yes | A list of enums of metrics to be fetched. Possible values are: `FORGE_API_REQUEST_COUNT` , `FORGE_API_REQUEST_LATENCY` , `FORGE_BACKEND_INVOCATION_COUNT` , `FORGE_BACKEND_INVOCATION_ERRORS`, `FORGE_BACKEND_INVOCATION_LATENCY`, `CONTAINER_CPU_USAGE_PERCENTAGE`, `CONTAINER_MEMORY_USAGE_PERCENTAGE`, `CONTAINER_UPTIME_SECONDS`, `CONTAINER_STATUS_RESTARTS_TOTAL`, and `SERVICE_INSTANCE_COUNT` |

#### Interval

Each API call retrieves at most 15 minutes of metrics. You can run a query for up to 14 days in the past.
This limit is enforced to make sure the number of data points returned is not huge in the API response.

We recommend fetching data periodically, for example, every three or five minutes. A rate limit of
five calls per minute per user is enforced.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `start` | `string` | Yes | Start time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format |
| `end` | `string` | Yes | End time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format |

## Set up your infrastructure

To consume the Atlassian GraphQL API and ingest metrics in real-time into observability tools,
we recommend having the following components in your infrastructure:

![Partner Server View](https://dac-static.atlassian.com/platform/forge/images/partner-server-arch.svg?_v=1.5800.2320)

### CronJob service

The CronJob service periodically polls the exposed GraphQL endpoint for the required metrics.
The AGG endpoint returns the OTLP protobuf JSON standard format as a response. The same response
is then pushed as is to the OTEL Sidecar, which is running alongside this cron service.

When setting up the service, you can use either a **serverless framework** or **server framework**.

#### Serverless framework

If using Amazon Web Services (AWS) infrastructure, you can configure Lambda to be executed
every “x” minutes or so. You can also use a similar configuration for Google Cloud Platform (GCP)
or Microsoft Azure infrastructure.

A sample Lambda configuration should look like the following:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
```



```
```
MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
    FunctionName: MyLambdaFunction
    Runtime: nodejs14.x
    Handler: index.handler
    Code:
        S3Bucket: my-function-bucket
        S3Key: my-function-package.zip
    Layers:
        - !Ref OTelLambdaLayer
    Environment:
        Variables:
        OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/config.yml
MyScheduledRule:
    Type: AWS::Events::Rule
    Properties:
    Description: My scheduled rule
    ScheduleExpression: rate(3 minutes)
    State: ENABLED
    Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
        Id: MyLambdaTarget
```
```
```

#### Server framework

If using AWS infrastructure, you can set up a dedicated EC2 resource running a server that polls
the AGG API every “x” minutes or so. This can be a virtual machine (VM) if running an on-premise
data center.

### OTEL Collector

Next, run an OTEL Collector/Sidecar using the configuration of three components:

1. **Receiver**: A receiver, which can be push- or pull-based, is how data gets into the OTEL Collector.
   An [OTLP receiver](https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md)
   is used, which can receive trace export calls via HTTP/JSON. The AGG response is compatible with
   the accepted format for this receiver to work.
2. **Processors**: Processors are run on data between being received and exported. While processors
   are optional, these are some of the
   [recommended ones](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor#recommended-processors).
3. **Exporters**: An exporter, which can be push- or pull-based, is how you send data to one or more
   backends or destinations. All supported exporters can be found
   [here](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

When setting up the service, you can use either a **serverless framework** or **server framework**.

#### Serverless framework

If using AWS infrastructure, you can leverage the OTEL lambda layer. You can also use a similar
configuration for GCP or Microsoft Azure infrastructure.

A sample configuration should look like the following:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
```



```
```
Resources:
OTelLambdaLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
    LayerName: OTelLambdaLayer
    Description: My OTEL Lambda layer
    Content:
        S3Bucket: my-layer-bucket
        S3Key: my-layer-package.zip
    CompatibleRuntimes:
        - nodejs14.x
MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
    FunctionName: MyLambdaFunction
    Runtime: nodejs14.x
    Handler: index.handler
    Code:
        S3Bucket: my-function-bucket
        S3Key: my-function-package.zip
    Layers:
        - !Ref OTelLambdaLayer
    Environment:
        Variables:
        OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/config.yml
MyScheduledRule:
    Type: AWS::Events::Rule
    Properties:
    Description: My scheduled rule
    ScheduleExpression: rate(3 minutes)
    State: ENABLED
    Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
        Id: MyLambdaTarget
```
```
```

#### Server framework

We recommend you run the OTEL Collector as a sidecar docker container on the same VM/EC2 server
responsible for cron scheduling.

To set up a server framework:

1. Create a sample `otel-collector-config.yaml` file in the repository as needed. The config file
   should look similar to this (we're using **SignalFX** as an example third-party monitoring tool here):

   ```
   ```
   1
   2
   3
   4
   5
   6
   7
   8
   9
   10
   11
   12
   13
   14
   15
   16
   17
   18
   19
   20
   21
   22
   23
   24
   ```



   ```
   receivers:
     otlp:
       protocols:
         http:
       
   exporters:
     signalfx:
       # Access token to send data to SignalFx.
       access_token: <access_token>
       # SignalFx realm where the data will be received.
       realm: us1
       # Timeout for the send operations.
       timeout: 30s  

   processors:
     batch:

   service:
     pipelines:
       metrics:
         receivers: [otlp]
         processors: [batch]
         exporters: [signalfx]
   ```
   ```
2. Create a Docker image with the open source OTEL collector
   [docker image](https://github.com/open-telemetry/opentelemetry-collector-contrib)
   available using: `docker build . -t otel-sidecar:v1`

   ```
   ```
   1
   2
   3
   4
   5
   6
   7
   8
   ```



   ```
   FROM otel/opentelemetry-collector-contrib:latest

   # Copy the collector configuration file into the container
   COPY otel-collector-config.yaml /etc/otel-collector-config.yaml

   # Start the collector with the specified configuration file
   CMD ["--config=/etc/otel-collector-config.yaml"]
   ```
   ```
3. Run the above Docker image: `docker run -p 4318:4318 otel-sidecar:v1`

   This will spin up the OTEL sidecar at `http://localhost:4318`.
4. Make an **HTTP POST** request with the response of the above AGG API endpoint, for example,
   `response.data.ecosystem.forgeMetrics.appMetrics`, to the sidecar running at path
   `http://localhost:4318/v1/metrics` on the same server.

   ```
   ```
   1
   2
   3
   4
   ```



   ```
   curl --location --request POST 'localhost:4318/v1/metrics' \
   --header 'Content-Type: application/json' \
   --data-raw '<response.data.ecosystem.forgeMetrics.appMetrics>'
   ```
   ```

App metrics should now be visible in your configured monitoring tool.

## Export API metrics

The following metrics are available for all `function` invocations making either
[Fetch API](/platform/forge/runtime-reference/fetch-api/),
[Async events API](/platform/forge/runtime-reference/async-events-api/),
and [Web trigger API](/platform/forge/runtime-reference/web-trigger-api/),
or [hosted storage API](/platform/forge/storage-reference/) HTTP requests
via the [App metrics API](/platform/forge/export-app-metrics/#query-the-app-metrics-api):

* **API request count**: The total number of HTTP requests, grouped by status codes, such as `2xx`,
  `3xx`, `4xx`, and `5xx`.
* **API request latency**: The round trip time it takes for a HTTP request triggered within
  a Forge function.

This doesn’t include code executing in a Custom UI iframe. However, this includes functions
invoked by `@forge/bridge`.

The following tags and dimensions are available with API metrics when using the App metrics API:

1. `remote`: Useful to bifurcate between Atlassian app, external, and GraphQL HTTP requests. This field
   can have one of the following values: `jira`, `confluence`, `bitbucket`, `egress`, or `stargate`.
2. `status`: Represents the HTTP status code received for an API call. This is only available
   for `API request count` metric.
3. `url`: Represents the path of the HTTP request. This field can have one of the following values,
   depending on the type of API call:

   * For non-Atlassian HTTP requests, `url` field will be captured as hostname.
     For example: `api.slack.com` , `api.google.com`
   * For Atlassian app HTTP requests, `url` field will have the templatized path, as such:
     `/rest/api/2/field/{fieldKey}/option` , `/repositories/{workspace}/{repo_slug}/commits`,
     `/rest/api/user/watch/content/{contentId}`
   * For Storage, GraphQL, and Async HTTP requests, the `url` field can have values as
     `/forge/entities/graphql`, `/graphql`,
     `/webhook/queue/publish/{cloudId}/{environmentId}/{appId}/{appVersion}`, and more.

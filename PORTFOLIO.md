# Portfolio description

## Korean

**Gaussian SLAM 자원 분석 및 압축 구현 최적화**

여러 SLAM 구현의 메모리 병목을 분석하고, 실제 삭제량과 공간별 quota를 통제한 압축 비교 실험을
수행한 프로젝트입니다. 정적 3DGS에서는 실제 삭제량을 맞추고, 오프라인 SLAM 압축에서는 공간별
quota와 정제 예산을 맞춰 점수를 비교했습니다. 9개 submap에서 압축 단계 시간을 평균 2.32초에서
0.99초로 줄였고(57.4%), 같은 입력의 삭제 mask 264건이 기존 구현과 일치했습니다. 이 단계 시간은
이전 통계 수집 비용을 제외합니다. 수집을 포함한 전체 비용과 품질 한계도 함께 검증하고, 분석 코드와
CPU 실행 예제, 실험 보고서를 공개용 자료로 정리했습니다.

## English

**Gaussian SLAM Resource Profiling and Compression Optimization**

This project profiles memory bottlenecks across Gaussian SLAM implementations and evaluates pruning scores
with controlled deletion budgets. Static 3DGS tests match actual deletion counts; offline SLAM tests match
per-voxel quotas and refinement work. On nine saved submaps, mean compression-stage time decreases from 2.32 s
to 0.99 s (57.4%), and 264 same-input removal-mask checks match the original implementation. These stage times
exclude earlier statistics collection. The study also evaluates collection-inclusive costs and quality
limitations, and provides analysis scripts, CPU examples and experiment reports.

## Evidence and scope

- [Reports and measured findings](README.md)
- [Cost, quality and failed controls](FOLLOW_UP.md)
- [Runnable numerical helpers](code/README.md)
- [AI assistance and license disclosure](README.md#ai-assistance-and-license)

The descriptions summarize the project. Individual contributions should be described according to the work
actually performed; implementation, execution, review and drafting used the AI assistance disclosed above.

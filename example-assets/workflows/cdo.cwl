cwlVersion: v1.0
class: CommandLineTool
hints:
  SoftwareRequirement:
    packages:
    - package: cdo

baseCommand: cdo
stdout: output.txt
inputs:
  op:
    type: string
    inputBinding:
      position: 1
  in_file:
    type: File
    inputBinding:
      position: 2
  out_name:
    type: string
    inputBinding:
      position: 3
outputs:
  stdout:
    type: string
    outputBinding:
      glob: output.txt
      loadContents: true
      outputEval: $(self[0].contents)
  out_file:
    type: File
    outputBinding:
      glob: $(inputs.out_name)


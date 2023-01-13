cwlVersion: v1.2
class: Workflow

inputs:
  message: string

outputs:
  out:
    type: string
    outputSource: double/output

steps:
  echo:
    run:
      class: CommandLineTool
      baseCommand: echo
      stdout: output.txt
      inputs:
        message:
          type: string
          inputBinding:
            position: 1
      outputs:
        output:
          type: string
          outputBinding:
            glob: output.txt
            loadContents: true
            outputEval: $(self[0].contents)

    in:
      message: message
    out: [output]
  double:
    run:
      class: CommandLineTool
      baseCommand: echo
      stdout: output.txt
      inputs:
        message:
          type: string
          inputBinding:
            position: 1
      outputs:
        output:
          type: string
          outputBinding:
            glob: output.txt
            loadContents: true
            outputEval: $(self[0].contents)
    in:
      message:
        source: echo/output
    out: [output]

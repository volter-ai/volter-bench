import * as React from "react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  uid: string
  skillName: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButtonBase = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ className, skillName, description, stats, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        className={cn("w-[200px]", className)}
        {...props}
      >
        {skillName}
      </Button>
    )
  }
)

SkillButtonBase.displayName = "SkillButton"

let SkillButton = withClickable(SkillButtonBase)

export { SkillButton }

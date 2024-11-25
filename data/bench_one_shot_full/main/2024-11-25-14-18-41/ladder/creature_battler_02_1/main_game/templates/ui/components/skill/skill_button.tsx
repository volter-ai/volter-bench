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

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, className, skillName, description, stats, ...props }, ref) => {
    return (
      <div className="space-y-2">
        <Button
          ref={ref}
          className={cn("w-full", className)}
          {...props}
        >
          {skillName}
          <div className="hidden group-hover:block absolute top-full mt-2 p-4 bg-popover rounded-md shadow-lg">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            <div className="flex gap-4 text-sm">
              {stats.damage && <p>Damage: {stats.damage}</p>}
              {stats.accuracy && <p>Accuracy: {stats.accuracy}%</p>}
              {stats.type && <p>Type: {stats.type}</p>}
            </div>
          </div>
        </Button>
      </div>
    )
  }
)

SkillButton.displayName = "SkillButton"

// Apply withClickable
SkillButton = withClickable(SkillButton)

export { SkillButton }

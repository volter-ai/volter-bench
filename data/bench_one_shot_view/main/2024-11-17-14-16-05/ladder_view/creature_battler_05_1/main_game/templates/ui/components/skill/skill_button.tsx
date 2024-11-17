import * as React from "react"
import { CustomHoverCard, CustomHoverCardContent, CustomHoverCardTrigger } from "@/components/ui/custom/hover-card"
import { CustomButton } from "@/components/ui/custom/button"
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
      <CustomHoverCard uid={uid}>
        <CustomHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <CustomButton
            uid={`${uid}-button`}
            ref={ref}
            className={cn("w-[200px]", className)}
            {...props}
          >
            {skillName}
          </CustomButton>
        </CustomHoverCardTrigger>
        <CustomHoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            <div className="flex gap-4 text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.type && <div>Type: {stats.type}</div>}
            </div>
          </div>
        </CustomHoverCardContent>
      </CustomHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }

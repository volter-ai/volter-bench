import * as React from "react"
import { CustomHoverCard, CustomHoverCardContent, CustomHoverCardTrigger } from "@/components/ui/custom/hover-card"
import { CustomButton } from "@/components/ui/custom/button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps extends React.ComponentProps<typeof CustomButton> {
  uid: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    type?: string
  }
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, children, description, stats, ...props }, ref) => {
    return (
      <CustomHoverCard uid={`${uid}-hover`}>
        <CustomHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <CustomButton ref={ref} uid={`${uid}-button`} {...props}>
            {children}
          </CustomButton>
        </CustomHoverCardTrigger>
        <CustomHoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <p className="text-sm">{description}</p>
            <div className="text-xs text-muted-foreground">
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

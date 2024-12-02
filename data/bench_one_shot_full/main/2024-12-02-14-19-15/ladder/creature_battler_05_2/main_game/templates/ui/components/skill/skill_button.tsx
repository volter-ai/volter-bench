import * as React from "react"
import { CustomHoverCard, CustomHoverCardContent, CustomHoverCardTrigger } from "@/components/ui/custom-hover-card"
import { CustomButton } from "@/components/ui/custom-button"
import withClickable from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  stats: {
    damage?: number
    accuracy?: number
    cost?: number
  }
  onClick?: () => void
  disabled?: boolean
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, stats, onClick, disabled, ...props }, ref) => {
    return (
      <CustomHoverCard uid={`${uid}-hover`}>
        <CustomHoverCardTrigger uid={`${uid}-trigger`} asChild>
          <CustomButton
            uid={`${uid}-button`}
            variant="secondary"
            onClick={onClick}
            disabled={disabled}
            className="w-full h-full"
            {...props}
          >
            {name}
          </CustomButton>
        </CustomHoverCardTrigger>
        <CustomHoverCardContent uid={`${uid}-content`} className="w-80">
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            <div className="text-sm">
              {stats.damage && <div>Damage: {stats.damage}</div>}
              {stats.accuracy && <div>Accuracy: {stats.accuracy}%</div>}
              {stats.cost && <div>Cost: {stats.cost}</div>}
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

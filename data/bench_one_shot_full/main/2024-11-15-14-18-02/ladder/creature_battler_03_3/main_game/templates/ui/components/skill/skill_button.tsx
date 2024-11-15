import * as React from "react"
import { Button } from "@/components/ui/button"
import { HoverCard, HoverCardTrigger, HoverCardContent } from "@/components/ui/hover-card"
import withClickable from "@/lib/withClickable"

// Create wrapped versions of base components
let CustomButton = withClickable(Button)
let CustomHoverCard = withClickable(HoverCard)
let CustomHoverCardTrigger = withClickable(HoverCardTrigger)
let CustomHoverCardContent = withClickable(HoverCardContent)

interface SkillButtonProps extends React.ComponentProps<typeof Button> {
  uid: string
  skillName: string
  description: string
  damage?: number
  accuracy?: number
  children?: React.ReactNode
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, skillName, description, damage, accuracy, children, ...props }, ref) => {
    return (
      <CustomHoverCard uid={uid}>
        <CustomHoverCardTrigger uid={uid} asChild>
          <CustomButton ref={ref} uid={uid} {...props}>
            {skillName}
          </CustomButton>
        </CustomHoverCardTrigger>
        <CustomHoverCardContent uid={uid}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{skillName}</h4>
            <p className="text-sm">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
          </div>
        </CustomHoverCardContent>
      </CustomHoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"

SkillButton = withClickable(SkillButton)

export { SkillButton }

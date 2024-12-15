import * as React from "react"
import { 
  HoverCard as ShadcnHoverCard, 
  HoverCardContent as ShadcnHoverCardContent, 
  HoverCardTrigger as ShadcnHoverCardTrigger 
} from "@/components/ui/hover-card"
import { Button as ShadcnButton } from "@/components/ui/button"
import { withClickable } from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  onClick?: () => void
}

interface WithUid {
  uid: string
}

let HoverCard = withClickable(ShadcnHoverCard) as React.FC<WithUid>
let HoverCardTrigger = withClickable(ShadcnHoverCardTrigger) as React.FC<WithUid>
let HoverCardContent = withClickable(ShadcnHoverCardContent) as React.FC<WithUid>
let Button = withClickable(ShadcnButton) as React.FC<WithUid>

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, onClick, ...props }, ref) => {
    return (
      <HoverCard uid={`${uid}-hover`}>
        <HoverCardTrigger uid={`${uid}-trigger`} asChild>
          <Button
            ref={ref}
            onClick={onClick}
            uid={uid}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm">{description}</p>
            {damage && <p className="text-sm">Damage: {damage}</p>}
            {accuracy && <p className="text-sm">Accuracy: {accuracy}%</p>}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"
SkillButton = withClickable(SkillButton)

export { SkillButton }

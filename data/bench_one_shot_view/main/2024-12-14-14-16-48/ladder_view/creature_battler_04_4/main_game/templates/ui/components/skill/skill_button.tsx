import * as React from "react"
import { Button } from "@/components/ui/button"
import { 
  HoverCard,
  HoverCardTrigger,
  HoverCardContent 
} from "@/components/ui/hover-card"
import { withClickable } from "@/lib/withClickable"

interface SkillButtonProps {
  uid: string
  name: string
  description: string
  damage?: number
  accuracy?: number
  children?: React.ReactNode
}

let SkillButton = React.forwardRef<HTMLButtonElement, SkillButtonProps>(
  ({ uid, name, description, damage, accuracy, children, ...props }, ref) => {
    return (
      <HoverCard uid={uid}>
        <HoverCardTrigger asChild uid={`${uid}-trigger`}>
          <Button
            variant="outline"
            className="w-[200px] h-[60px]"
            ref={ref}
            uid={`${uid}-button`}
            {...props}
          >
            {name}
          </Button>
        </HoverCardTrigger>
        <HoverCardContent className="w-80" uid={`${uid}-content`}>
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">{name}</h4>
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
            {damage && (
              <p className="text-sm">Damage: {damage}</p>
            )}
            {accuracy && (
              <p className="text-sm">Accuracy: {accuracy}%</p>
            )}
          </div>
        </HoverCardContent>
      </HoverCard>
    )
  }
)

SkillButton.displayName = "SkillButton"
SkillButton = withClickable(SkillButton)

export { SkillButton }

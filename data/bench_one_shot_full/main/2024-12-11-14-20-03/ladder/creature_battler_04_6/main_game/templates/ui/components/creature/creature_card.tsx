import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

let BaseCard = Card
let BaseCardContent = CardContent
let BaseCardHeader = CardHeader
let BaseCardTitle = CardTitle

// Wrap base components
BaseCard = withClickable(BaseCard)
BaseCardContent = withClickable(BaseCardContent)
BaseCardHeader = withClickable(BaseCardHeader)
BaseCardTitle = withClickable(BaseCardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`}>
          <img
            src={image}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <Progress value={(currentHp / maxHp) * 100} uid={`${uid}-progress`} />
          <div className="text-sm text-right mt-1">
            {currentHp}/{maxHp} HP
          </div>
        </BaseCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

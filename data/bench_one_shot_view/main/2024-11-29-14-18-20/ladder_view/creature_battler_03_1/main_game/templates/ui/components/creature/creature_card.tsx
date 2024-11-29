import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCardHeader = withClickable(CardHeader)
let CreatureCardContent = withClickable(CardContent)
let CreatureCardTitle = withClickable(CardTitle)
let BaseCard = withClickable(Card)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <BaseCard ref={ref} className={cn("w-[300px]", className)} uid={uid} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CreatureCardContent>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

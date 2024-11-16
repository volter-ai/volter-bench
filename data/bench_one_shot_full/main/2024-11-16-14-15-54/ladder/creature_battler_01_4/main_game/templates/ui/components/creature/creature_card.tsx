import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let BaseCard = withClickable(Card)
let BaseCardHeader = withClickable(CardHeader)
let BaseCardTitle = withClickable(CardTitle)
let BaseCardDescription = withClickable(CardDescription)
let BaseCardContent = withClickable(CardContent)
let BaseCardFooter = withClickable(CardFooter)

interface CreatureCardProps extends BaseCardProps {
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <BaseCard ref={ref} className={cn("w-[350px]", className)} uid={uid} {...props}>
        <BaseCardHeader uid={`${uid}-header`}>
          <BaseCardTitle uid={`${uid}-title`}>{name}</BaseCardTitle>
          <BaseCardDescription uid={`${uid}-desc`}>HP: {hp}/{maxHp}</BaseCardDescription>
        </BaseCardHeader>
        <BaseCardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
        </BaseCardContent>
        <BaseCardFooter uid={`${uid}-footer`} className="flex justify-between">
        </BaseCardFooter>
      </BaseCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseComponentProps>(
  ({ uid, ...props }, ref) => <BaseCard ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseComponentProps>(
  ({ uid, ...props }, ref) => <BaseCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLDivElement, BaseComponentProps>(
  ({ uid, ...props }, ref) => <BaseCardTitle ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseComponentProps>(
  ({ uid, ...props }, ref) => <BaseCardContent ref={ref} {...props} />
)

Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

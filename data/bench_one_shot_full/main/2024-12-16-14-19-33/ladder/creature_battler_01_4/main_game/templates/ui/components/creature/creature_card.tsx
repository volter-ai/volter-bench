import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader,
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement> & BaseProps>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

Card.displayName = "Card"
CardContent.displayName = "CardContent"
CardHeader.displayName = "CardHeader"
CardTitle.displayName = "CardTitle"

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

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
      <Card uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="flex justify-between items-center">
              <span>HP:</span>
              <span>{hp}/{maxHp}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }

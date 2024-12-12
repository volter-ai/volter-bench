import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCard>>(
  ({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCardContent>>(
  ({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnCardHeader>>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseProps & React.ComponentProps<typeof ShadcnCardTitle>>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />
)

let Progress = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentProps<typeof ShadcnProgress>>(
  ({ uid, ...props }, ref) => <ShadcnProgress ref={ref} {...props} />
)

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
Progress = withClickable(Progress)

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
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-48 object-contain mb-4"
          />
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>HP</span>
              <span>{hp}/{maxHp}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(hp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
